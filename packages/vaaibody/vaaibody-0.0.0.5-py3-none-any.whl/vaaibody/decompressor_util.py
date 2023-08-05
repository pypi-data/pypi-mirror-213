import numpy as np
import torch
from scipy.spatial.transform import Rotation as R

from vaaibody.core.motion import Motion
from vaaibody.core.skeleton import Transform
from vaaibody.utilities.frame_utils import get_angular_vel, get_position_vel


def get_positions_from_motion(motion: Motion):
    skel = motion.skeleton
    n_joint = skel.num_joints()
    frm_time = motion.frame_time

    bone_positions = []
    for idx_frame in range(len(motion)):
        pose = np.zeros(n_joint * 3)
        for idx_joint in range(n_joint):
            if idx_joint == 0:
                # cur_pos = motion[idx_frame].get_global_transform(idx_joint).translation
                cur_pos = motion[idx_frame].get_local_transform(idx_joint).translation
            else:
                cur_pos = motion[idx_frame].get_local_transform(idx_joint).translation
            pose[3 * idx_joint : 3 * (idx_joint + 1)] = cur_pos
        bone_positions.append(pose)
    return np.array(bone_positions, dtype="f")


def get_quat_rotations_from_motion(motion: Motion):
    n_joint = 61
    rotations = []
    for idx_frame in range(len(motion)):
        rot_joints = []
        for idx_joint in range(n_joint):
            rot_joints.append(
                motion[idx_frame].get_local_transform(idx_joint).rotation.as_quat()
            )
        rotations.append(rot_joints)
    return np.array(rotations, dtype="f")


def get_local_transform_from_posrot(poses, rots):
    n_frame = len(poses)
    n_joint = 61
    local_transforms = list()
    for idx_frame in range(n_frame):
        local_tranforms_frame = list()
        for idx_joint in range(n_joint):
            cur_transform = Transform(
                R.from_quat(rots[idx_frame][idx_joint]), poses[idx_frame][idx_joint]
            )
            local_tranforms_frame.append(cur_transform)
        local_transforms.append(local_tranforms_frame)
    return local_transforms


def get_Y(motion_database, n_motion, n_joint, frame_size):
    Ypos = []
    Yrot = []
    Yvel = []
    Yang = []

    for idx_motion in range(n_motion):
        motion = motion_database.get_motion(idx_motion)
        motion_n_frame = motion.num_frame

        num_len = motion.num_frame() // frame_size
        if num_len == 0:
            num_len = 1
        Ypos += list(get_positions_from_motion(motion).reshape(-1, n_joint, 3))[
            : num_len * frame_size
        ]
        Yrot += list(get_quat_rotations_from_motion(motion))[: num_len * frame_size]
        Yvel += list(get_position_vel(motion).reshape(-1, n_joint, 3))[
            : num_len * frame_size
        ]
        Yang += list(get_angular_vel(motion).reshape(-1, n_joint, 3))[
            : num_len * frame_size
        ]

    Ypos = np.array(Ypos)
    Yrot = np.array(Yrot)
    Yvel = np.array(Yvel)
    Yang = np.array(Yang)

    return Ypos, Yrot, Yvel, Yang


def get_X(feature_database):
    X = []
    clip_idx_list = []
    for idx_motion in range(len(feature_database.pose_feature)):
        n_seq, n_window, _ = np.array(feature_database.pose_feature[idx_motion]).shape
        if idx_motion == 0:
            clip_idx_list.append((0, n_seq * n_window))
        else:
            clip_idx_list.append(
                (clip_idx_list[-1][1], clip_idx_list[-1][1] + n_seq * n_window)
            )
        for idx_seq in range(len(feature_database.pose_feature[idx_motion])):
            X += list(feature_database.pose_feature[idx_motion][idx_seq])
    X = np.array(X)
    return X, clip_idx_list


def get_parents_list(motion_database):
    # Prepare Parents
    # parents [-1, 0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10,
    #  11, 12, 13, 14, 15, 16, 17, 18, 16, 20, 21, 22,
    #  16, 24, 25, 26, 16, 28, 29, 30, 16, 32, 33, 34,
    #  12, 36, 12, 38, 39, 40, 41, 42, 43, 41, 45, 46,
    #  47, 41, 49, 50, 51, 41, 53, 54, 55, 41, 57, 58, 59]
    joint_dict = motion_database.get_motion(0).skeleton.joint_dict

    parents = []
    for joint_name in joint_dict.keys():
        parent = (
            motion_database.get_motion(0).skeleton.get_joint_by_name(joint_name).parent
        )
        if parent:
            parents.append(parent.idx)
        else:
            parents.append(-1)

    return parents


# Function to save compressed database
def save_compressed_database(
    network_compressor, input, n_frame, mean, std, feature_database
):
    # todo
    # sequence padding etc
    Ypos, Ytxy, Yvel, Yang, Qpos, Qtxy, Qvel, Qang = input

    with torch.no_grad():
        Z = (
            network_compressor(
                (
                    torch.cat(
                        [
                            Ypos[:, 1:].reshape([1, n_frame, -1]),
                            Ytxy[:, 1:].reshape([1, n_frame, -1]),
                            Yvel[:, 1:].reshape([1, n_frame, -1]),
                            Yang[:, 1:].reshape([1, n_frame, -1]),
                            Qpos[:, 1:].reshape([1, n_frame, -1]),
                            Qtxy[:, 1:].reshape([1, n_frame, -1]),
                            Qvel[:, 1:].reshape([1, n_frame, -1]),
                            Qang[:, 1:].reshape([1, n_frame, -1]),
                            # Yrvel.reshape([1, n_frame, -1]),
                            # Yrang.reshape([1, n_frame, -1]),
                        ],
                        dim=-1,
                    )
                    - mean
                )
                / std
            )[0]
            .cpu()
            .numpy()
        )

        # Z - (n_frame, n_feature)
        # reshape to (n_motion, n_seq, n_seq_size, n_feature)
        latent_feature = []
        cur_frame = 0
        seq_size = 300

        # sil 일때는 따로 처리

        if np.array(feature_database.pose_feature[0]).shape[0] == 1:  # (1, 71, 513)
            for idx_motion in range(len(feature_database.pose_feature)):
                length_motion = len(feature_database.pose_feature[idx_motion])
                latent_feature.append(Z[cur_frame : cur_frame + length_motion])
                cur_frame += length_motion

        else:
            for idx_motion in range(
                len(feature_database.pose_feature)
            ):  # (78, 300, 513)
                seq_feature = []
                for idx_seq in range(len(feature_database.pose_feature[idx_motion])):
                    seq_feature.append(
                        Z[
                            cur_frame
                            + idx_seq * seq_size : cur_frame
                            + (idx_seq + 1) * seq_size
                        ]
                    )
                cur_frame += 300 * (idx_seq + 1)
                latent_feature.append(seq_feature)

        # latent_feature = np.array(latent_feature)
        # feature_database

        # todo
        # Write latent variables
        import pickle

        with open("latentFeature.pickle", "wb") as fw:
            pickle.dump(latent_feature, fw)


def get_decompressor_mean_std(Ypos, Ytxy, Yvel, Yang):
    decompressor_mean_out = torch.as_tensor(
        np.hstack(
            [
                Ypos[:, 1:].mean(axis=0).ravel(),
                Ytxy[:, 1:].mean(axis=0).ravel(),
                Yvel[:, 1:].mean(axis=0).ravel(),
                Yang[:, 1:].mean(axis=0).ravel(),
                # Yrvel.mean(axis=0).ravel(),
                # Yrang.mean(axis=0).ravel(),
            ]
        ).astype(np.float32)
    )

    decompressor_std_out = torch.as_tensor(
        np.hstack(
            [
                Ypos[:, 1:].std(axis=0).ravel(),
                Ytxy[:, 1:].std(axis=0).ravel(),
                Yvel[:, 1:].std(axis=0).ravel(),
                Yang[:, 1:].std(axis=0).ravel(),
                # Yrvel.std(axis=0).ravel(),
                # Yrang.std(axis=0).ravel(),
            ]
        ).astype(np.float32)
    )
    return decompressor_mean_out, decompressor_std_out


def get_compressor_mean_std(
    Ypos,
    Ytxy,
    Yvel,
    Yang,
    Qpos,
    Qtxy,
    Qvel,
    Qang,
    Ypos_scale,
    Ytxy_scale,
    Yvel_scale,
    Yang_scale,
    Qpos_scale,
    Qtxy_scale,
    Qvel_scale,
    Qang_scale,
    n_joint,
):
    compressor_mean_in = torch.as_tensor(
        np.hstack(
            [
                Ypos[:, 1:].mean(axis=0).ravel(),
                Ytxy[:, 1:].mean(axis=0).ravel(),
                Yvel[:, 1:].mean(axis=0).ravel(),
                Yang[:, 1:].mean(axis=0).ravel(),
                Qpos[:, 1:].mean(axis=0).ravel(),
                Qtxy[:, 1:].mean(axis=0).ravel(),
                Qvel[:, 1:].mean(axis=0).ravel(),
                Qang[:, 1:].mean(axis=0).ravel(),
                # Yrvel.mean(axis=0).ravel(),
                # Yrang.mean(axis=0).ravel(),
            ]
        ).astype(np.float32)
    )

    compressor_std_in = torch.as_tensor(
        np.hstack(
            [
                Ypos_scale.repeat((n_joint - 1) * 3),
                Ytxy_scale.repeat((n_joint - 1) * 6),
                Yvel_scale.repeat((n_joint - 1) * 3),
                Yang_scale.repeat((n_joint - 1) * 3),
                Qpos_scale.repeat((n_joint - 1) * 3),
                Qtxy_scale.repeat((n_joint - 1) * 6),
                Qvel_scale.repeat((n_joint - 1) * 3),
                Qang_scale.repeat((n_joint - 1) * 3),
                # Yrvel_scale.repeat(3),
                # Yrang_scale.repeat(3),
            ]
        ).astype(np.float32)
    )
    return compressor_mean_in, compressor_std_in
