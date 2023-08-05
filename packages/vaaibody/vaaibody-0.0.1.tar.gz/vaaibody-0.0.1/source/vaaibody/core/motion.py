import linecache
import os
import time
from tqdm import tqdm
from copy import deepcopy
from pathlib import Path

import natsort
import numpy as np
from scipy.spatial.transform import Rotation as R

from vaaibody.core.frame import Frame
from vaaibody.core.skeleton import Skeleton, Transform


def load_frame_from_bvh(file_path, idx, default_lines):
    """
    idx에 해당하는 frame line load
    """
    line = linecache.getline(file_path, idx + default_lines)
    line = line.strip()
    frame = np.array([float(f) for f in line.split(" ")])
    return np.array([frame])


def load_frame_time_from_bvh(file_path):
    pre_load = 0
    with open(file_path, "r") as bvh:
        while True:
            line = bvh.readline()
            pre_load += 1
            if not line:
                break
            if line[:6].upper() == "MOTION":
                break

        # num frame
        line = bvh.readline()
        line = line.strip()
        num_frame = int(line[7:].strip())

        # frame time
        line = bvh.readline()
        line = line.strip()
        frame_time = float(line[12:])
        pre_load += 2
        return frame_time, pre_load


def load_motion_from_bvh(file_path):
    """
    bvh 파일의 MOTION 이하 부분 파싱

    MOTION
    Frames:
    Frame Time:
    ~
    """
    with open(file_path, "r") as bvh:
        while True:
            line = bvh.readline()
            if not line:
                break
            if line[:6].upper() == "MOTION":
                break

        # num frame
        line = bvh.readline()
        line = line.strip()
        num_frame = int(line[7:].strip())

        # frame time
        line = bvh.readline()
        line = line.strip()
        frame_time = float(line[12:])

        # motions
        frames = []
        while True:
            line = bvh.readline()
            if not line:
                break
            line = line.strip()
            frame = np.array([float(f) for f in line.split(" ")])
            frames.append(frame)

        return np.array(frames), frame_time


def convert_from_bvh(skel, frames, return_type="transform"):
    batch_local_transforms = [
        Transform() for _ in range(skel.num_joints())
    ]  # Transform shape = (n_frame,)
    batch_global_transforms = [Transform() for _ in range(skel.num_joints())]

    if "Hips" in skel.joint_dict:
        root_name = "Hips"
    elif "Hip" in skel.joint_dict:
        root_name = "Hip"
    elif "root" in skel.joint_dict:
        root_name = "root"
    elif "body_world" in skel.joint_dict:
        root_name = "b_spine0"

    # convert euler to frames
    for i, joint in enumerate(skel.joints):
        # TODO : assume all channels are same
        if joint.dof == 6:
            if i == 0:
                translation = (
                    frames[:, joint.idx_in_skeleton : joint.idx_in_skeleton + 3] / 100.0
                )
            else:
                translation = np.ones_like(frames[:, 0:3])
                translation = joint.default_offset * translation

            rotation = R.from_euler(
                skel._rot,
                frames[:, joint.idx_in_skeleton + 3 : joint.idx_in_skeleton + 6],
                degrees=True,
            )

        elif joint.dof == 3:
            translation = joint.default_offset
            rotation = R.from_euler(
                skel._rot,
                frames[:, joint.idx_in_skeleton : joint.idx_in_skeleton + 3],
                degrees=True,
            )
        else:
            print("unspecified joint dof")
            exit(0)

        batch_local_transforms[i].translation = translation
        batch_local_transforms[i].rotation = rotation

        if i == 0:
            batch_global_transforms[i] = batch_local_transforms[i]
        else:
            batch_global_transforms[i] = (
                batch_global_transforms[skel.joint_dict[joint.parent.name]]
                * batch_local_transforms[i]
            )

    # root decomposition
    hips = deepcopy(batch_global_transforms[skel.joint_dict[root_name]])

    # predefined based on skeleton
    # 데이터가 바뀌면 이걸 바꿔야 할 수 있음
    # base root을 따로 정의하고 표현함.
    base_forward_axis = np.array([0, -1, 0])
    base_up_axis = np.array([1, 0, 0])
    base_right_axis = np.array([0, 0, -1])

    batch_root_rotation = hips.rotation

    axis_z = batch_root_rotation.apply(base_forward_axis)
    axis_y = batch_root_rotation.apply(base_up_axis)
    axis_x = batch_root_rotation.apply(base_right_axis)

    batch_root_rotation = R.from_matrix(np.stack([axis_x, axis_y, axis_z], axis=-1))

    adjust_angle = np.arccos(axis_y[:, 1])
    adjust_axis = np.cross(axis_y, np.array([0, 1, 0]))
    adjust_axis = adjust_axis / np.linalg.norm(adjust_axis, axis=-1, keepdims=True)
    adjust_rotation = R.from_rotvec(adjust_angle.reshape((-1, 1)) * adjust_axis)

    batch_root_rotation = adjust_rotation * batch_root_rotation

    batch_root_translation = hips.translation
    batch_root_translation[:, 1] = 0

    batch_root_transforms = Transform(
        batch_root_rotation.as_matrix(), batch_root_translation
    )
    batch_root_transforms_inv = batch_root_transforms.inverse()

    batch_local_transforms[0] = batch_root_transforms_inv * batch_local_transforms[0]
    batch_component_transforms = [Transform() for _ in range(skel.num_joints())]
    batch_body_global_transforms = [Transform() for _ in range(skel.num_joints())]
    for i in range(skel.num_joints()):
        batch_component_transforms[i] = (
            batch_root_transforms_inv * batch_global_transforms[i]
        )
        batch_body_global_transforms[i] = (
            batch_global_transforms[i] * skel.joints[i].body_transform
        )

    num_frame = len(batch_local_transforms[0])

    if return_type == "numpy":  # return as a numpy type
        batch_local_rot = []
        batch_local_trans = []
        batch_global_rot = []
        batch_global_trans = []
        batch_component_rot = []
        batch_component_trans = []
        batch_body_global_rot = []
        batch_body_global_trans = []
        for i in range(len(batch_local_transforms)):
            batch_local_rot.append(batch_local_transforms[i].rotation_np)
            batch_local_trans.append(batch_local_transforms[i].translation)
            batch_global_rot.append(batch_global_transforms[i].rotation_np)
            batch_global_trans.append(batch_global_transforms[i].translation)
            batch_component_rot.append(batch_component_transforms[i].rotation_np)
            batch_component_trans.append(batch_component_transforms[i].translation)
            batch_body_global_rot.append(batch_body_global_transforms[i].rotation_np)
            batch_body_global_trans.append(batch_body_global_transforms[i].translation)

        # swapaxes: (n_joint, n_frame ,...) -> (n_frame, n_joint, ...)
        return [
            batch_root_transforms.rotation_np,
            batch_root_transforms.translation,
            np.swapaxes(np.array(batch_local_rot), 0, 1),
            np.swapaxes(np.array(batch_local_trans), 0, 1),
            batch_root_transforms_inv.rotation_np,
            batch_root_transforms_inv.translation,
            np.swapaxes(np.array(batch_global_rot), 0, 1),
            np.swapaxes(np.array(batch_global_trans), 0, 1),
            np.swapaxes(np.array(batch_component_rot), 0, 1),
            np.swapaxes(np.array(batch_component_trans), 0, 1),
            np.swapaxes(np.array(batch_body_global_rot), 0, 1),
            np.swapaxes(np.array(batch_body_global_trans), 0, 1),
        ]

    else:
        converted_frames = (
            []
        )  # converted_frames shape = (n_frame, Frame=(n_joint, ...))
        for idx_frame in range(num_frame):
            root_transform = batch_root_transforms[idx_frame]
            local_transforms = [
                local_trans[idx_frame] for local_trans in batch_local_transforms
            ]
            root_transform_inv = batch_root_transforms_inv[idx_frame]
            global_transforms = [
                global_trans[idx_frame] for global_trans in batch_global_transforms
            ]
            component_transforms = [
                component_trans[idx_frame]
                for component_trans in batch_component_transforms
            ]
            body_global_transforms = [
                body_global_trans[idx_frame]
                for body_global_trans in batch_body_global_transforms
            ]
            frame = Frame(
                skel,
                root_transform,
                local_transforms,
                root_transform_inv,
                global_transforms,
                component_transforms,
                body_global_transforms,
                True,
            )
            converted_frames.append(frame)
        return converted_frames


class Motion:
    def __init__(self, skeleton, frames=None, frame_time=None, file_path=None):
        self._skeleton = skeleton
        self._frames = frames  # frame정보가 bvh파일을 읽고, 이를 transform형태로 변환하여 list에 저장한 형태
        # self._tuple_frame = None
        self._frame_time = frame_time
        self._file_path = file_path
        self._raw_frames = []  # frame 정보가 bvh파일에서 frames를 읽고 그대로 list에 저장한 형태

        if self._frames is not None and self._frame_time is not None:
            self.is_loaded = True
        elif self._file_path is not None:
            self.is_loaded = False
            # self.preload()
        else:
            print("Data should be given")
            exit(0)

    # def preload(self):
    #     self._raw_frames, self._frame_time = load_motion_from_bvh(self._file_path)

    def load_frame(self, idx):
        if self._frame_time is None:
            self._frame_time, self.time_line = load_frame_time_from_bvh(self._file_path)
        raw_frame = load_frame_from_bvh(self._file_path, idx, self.time_line)
        frame = convert_from_bvh(self._skeleton, raw_frame)

        return frame[0]

    def load_data(self):
        if self._frames is None:
            raw_frames, self._frame_time = load_motion_from_bvh(self._file_path)
            self._frames = convert_from_bvh(self._skeleton, raw_frames)
            self.is_loaded = True

    def copy(self):
        self.load_data()
        frames = [frame.copy() for frame in self._frames]
        new_motion = Motion(self._skeleton, frames=frames, frame_time=self._frame_time)
        new_motion._file_path = self._file_path
        return new_motion

    def __str__(self):
        self.load_data()
        return "Num frame : {}, Skeleton : {}, Path : {}".format(
            self.num_frame(), self._skeleton.name, self._file_path
        )

    def set_skeleton(self, skel):
        self._skeleton = skel
        if self._frames is not None:
            for f in self._frames:
                f._skeleton = skel

    @property
    def frame_time(self):
        self.load_data()
        return self._frame_time

    @property
    def file_path(self):
        return self._file_path

    @property
    def skeleton(self):
        return self._skeleton

    def num_frame(self):
        self.load_data()
        return len(self._frames)

    def __getitem__(self, idx):
        if self.is_loaded:
            return self._frames[idx]
        else:
            return self.load_frame(idx)

    def __add__(self, next_motion):
        self.load_data()
        new_motion = self.copy()
        new_motion.append(next_motion)
        new_motion._file_path = ""
        return new_motion

    def append(self, next_motion):
        self.load_data()
        for f in range(next_motion.num_frame()):
            self._frames.append(next_motion[f].copy())

    def add_frame(self, new_frame):
        self.load_data()
        self._frames.append(new_frame)

    def cut_frame(self, idx_st=0, idx_end=None):
        self.load_data()
        if idx_end == None:
            idx_end = self.num_frame()
        self._frames = self._frames[idx_st:idx_end]

    def __len__(self):
        return self.num_frame()

    def __iter__(self):
        self.load_data()
        return iter(self._frames)


class MotionDatabase:
    def __init__(
        self, skeleton, dir_path="", motions=[], is_preload=False, use_npz=False
    ):
        self._skeleton = skeleton
        self._dir_path = dir_path
        self._use_npz = use_npz
        self._motions = []

        if dir_path == "":
            assert len(motions) > 0
            self.create_db_from_motions(motions)
        elif self._use_npz:
            self.preload_db_with_npz(self._dir_path)
        elif is_preload:
            self.preload_db_with_bvh(self._dir_path)
        else:
            self.load_db(self._dir_path)

    @property
    def dir_path(self):
        return self._dir_path

    def num_motion(self):
        return len(self._motions)

    def get_frame(self, motion_idx, frame_idx):
        return self._motions[motion_idx][frame_idx]

    def modify_motion(self, idx, motion):
        self._motions[idx] = motion

    def append_motion(self, motion):
        self._motions.append(motion)

    def get_motion(self, idx):
        return self._motions[idx]

    def get_motion_len(self, idx):
        return len(self._motions[idx])

    def get_motion_by_name(self, name):
        for m in self._motions:
            if m._file_path == ("{}/{}".format(self._dir_path, name)):
                return m
        return None

    def get_idx_motion_by_name(self, name):
        if self._use_npz:
            name = name + ".npz"
        else:
            name = name + ".bvh"
        for idx, m in enumerate(self._motions):
            if "{}/{}".format(self._dir_path, name) == m._file_path:
                return idx, m
        return None

    def get_idx_motion(self, motion: Motion):
        path = motion.file_path
        for idx, m in enumerate(self._motions):
            if path == m._file_path:
                return idx
        return None

    def get_frame_time(
        self,
    ):
        if len(self._motions) == 0:
            self.load_db(self._dir_path)
        return self._motions[0].frame_time

    def create_db_from_motions(self, motions):
        self._motions = motions

    def load_db(self, dir_path):
        self._motions = []
        if os.path.exists(dir_path):
            for file_path in natsort.natsorted(os.listdir(dir_path)):
                if file_path.endswith(".bvh"):
                    path = "{}/{}".format(dir_path, file_path)
                    self._motions.append(Motion(self._skeleton, file_path=path))

    def preload_db_with_npz(self, dir_path):
        if os.path.exists(dir_path):
            print("Reading numpy files in the motion folder")
            self._motions = []
            frame_time = None

            for file_path in tqdm(natsort.natsorted(os.listdir(dir_path))):
                if file_path.endswith(".npz"):
                    path = "{}/{}".format(dir_path, file_path)
                    arr_from_npz = np.load(path)

                    if frame_time is None:
                        frame_time = arr_from_npz["arr_12"][0]

                    # matrix_order = ("root_transform", "local_transform", "root_transform_inv", "global_transform", "component_transform", "global_transform")
                    root_transform_rot = arr_from_npz["arr_0"]
                    root_transform_trans = arr_from_npz["arr_1"]
                    local_transform_rot = arr_from_npz["arr_2"]
                    local_transform_trans = arr_from_npz["arr_3"]
                    root_transform_inv_rot = arr_from_npz["arr_4"]
                    root_transform_inv_trans = arr_from_npz["arr_5"]
                    global_transform_rot = arr_from_npz["arr_6"]
                    global_transform_trans = arr_from_npz["arr_7"]
                    component_transform_rot = arr_from_npz["arr_8"]
                    component_transform_trans = arr_from_npz["arr_9"]
                    body_global_transform_rot = arr_from_npz["arr_10"]
                    body_global_transform_trans = arr_from_npz["arr_10"]

                    arr_from_npz.close()
                    new_frames = []
                    tot_frames_num = len(root_transform_rot)
                    for idx_frame in range(tot_frames_num):
                        root_transform = Transform(
                            root_transform_rot[idx_frame],
                            root_transform_trans[idx_frame],
                        )
                        local_transform = [
                            Transform(
                                local_transform_rot[idx_frame][idx_joint],
                                local_transform_trans[idx_frame][idx_joint],
                            )
                            for idx_joint in range(self._skeleton.num_joints())
                        ]
                        root_transform_inv = Transform(
                            root_transform_inv_rot[idx_frame],
                            root_transform_inv_trans[idx_frame],
                        )
                        global_transform = [
                            Transform(
                                global_transform_rot[idx_frame][idx_joint],
                                global_transform_trans[idx_frame][idx_joint],
                            )
                            for idx_joint in range(self._skeleton.num_joints())
                        ]
                        component_transform = [
                            Transform(
                                component_transform_rot[idx_frame][idx_joint],
                                component_transform_trans[idx_frame][idx_joint],
                            )
                            for idx_joint in range(self._skeleton.num_joints())
                        ]
                        body_global_transform = [
                            Transform(
                                body_global_transform_rot[idx_frame][idx_joint],
                                body_global_transform_trans[idx_frame][idx_joint],
                            )
                            for idx_joint in range(self._skeleton.num_joints())
                        ]
                        fr = Frame(
                            self._skeleton,
                            root_transform,
                            local_transform,
                            root_transform_inv,
                            global_transform,
                            component_transform,
                            body_global_transform,
                            True,
                        )
                        new_frames.append(fr)
                    self._motions.append(
                        Motion(
                            self._skeleton,
                            frames=new_frames,
                            frame_time=frame_time,
                            file_path=path,
                        )
                    )
        else:
            # npz 생성하기 코드로 이어도 됨
            print("Invalid npz folder")

    def convert_bvh_to_npz(self, dir_path, save_path_db):  # save만 하는 함수
        """
        bvh파일을 열어서 필요한 translation, rotation 정보를 추출하고 npz형태로 저장
        """
        start_time = time.time()
        if os.path.exists(dir_path):
            bvh_file_paths = []
            frames = []  # 모든 파일의 frame 정보가 담긴 list
            frame_time = None
            print("Reading files in the motion folder")
            for file_path in natsort.natsorted(os.listdir(dir_path)):
                if file_path.endswith(".bvh"):
                    path = "{}/{}".format(dir_path, file_path)
                    frs, ft = load_motion_from_bvh(path)
                    if frame_time is None:
                        frame_time = ft
                    elif frame_time != ft:
                        print(
                            "Frame time is not same : prev - {}s, {} - {}s".format(
                                frame_time, file_path, ft
                            )
                        )
                    bvh_file_paths.append(Path(file_path))
                    frames.append(frs)

            concatenated_frames = np.concatenate(frames, axis=0)
            converted_frames = convert_from_bvh(
                self._skeleton, concatenated_frames, return_type="numpy"
            )  # shape=(12, frame_num, joint_num, ...)

            self._motions = []
            start = 0
            # mtx_names = ["local_rot", "local_trans", "global_rot"]
            print("Loading the motion DB")
            for idx_file, frame in enumerate(frames):
                end = start + len(frame)
                save_file_path = Path(save_path_db) / bvh_file_paths[idx_file].stem
                # mtx_dict =  dict.fromkeys(mtx_names)
                mtx_list = []
                for j, mtx in enumerate(converted_frames):
                    mtx_list.append(mtx[start:end])
                mtx_list.append(np.array([frame_time]))

                np.savez_compressed(
                    save_file_path, *mtx_list
                )  # you can choose npz format e.g)np.savez()
                start = end

            print("Motion DB load : {} seconds".format(time.time() - start_time))

    def preload_db_with_bvh(self, dir_path):
        start_time = time.time()
        if os.path.exists(dir_path):
            paths = []
            frames = []
            frame_time = None
            print("Reading files in the motion folder")
            for file_path in tqdm(natsort.natsorted(os.listdir(dir_path))):
                if file_path.endswith(".bvh"):
                    path = "{}/{}".format(dir_path, file_path)
                    frs, ft = load_motion_from_bvh(path)
                    if frame_time is None:
                        frame_time = ft
                    elif frame_time != ft:
                        print(
                            "Frame time is not same : prev - {}s, {} - {}s".format(
                                frame_time, file_path, ft
                            )
                        )
                    paths.append(path)
                    frames.append(frs)
            concatenated_frames = np.concatenate(
                frames, axis=0
            )  # shape=(n_frames, dof*num_joint)
            converted_frames = convert_from_bvh(self._skeleton, concatenated_frames)

            self._motions = []
            start = 0
            print("Loading the motion DB")
            for i, f in enumerate(frames):
                end = start + len(f)
                self._motions.append(
                    Motion(
                        self._skeleton,
                        frames=converted_frames[start:end],
                        frame_time=frame_time,
                        file_path=paths[i],
                    )
                )
                start = end

            print("Motion DB load : {} seconds".format(time.time() - start_time))
        else:
            print("Motion DB load error : Invalid path")


if __name__ == "__main__":
    skel = Skeleton(name="goninA")
    skel.load_hierarchy_from_bvh("data/motion/goninA/goninA_run.bvh")
    db = MotionDatabase(skel, "data/motion/goninA")
