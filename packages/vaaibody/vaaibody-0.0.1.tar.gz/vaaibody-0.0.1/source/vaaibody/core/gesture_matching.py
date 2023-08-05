import time
from typing import Optional, Tuple

import numpy as np
from sklearn.metrics import pairwise_distances

# from decompressor_util import get_local_transform_from_posrot
from parameter.gesture_matching_parameter import MCS_SPINES
from scipy import spatial
from sklearn.neighbors import KDTree
from tqdm import tqdm
from vaaibody.utilities import quat
from vaaibody.utilities.frame_utils import filter_frames
from vaaibody.utilities.timechecker import TimeChecker as TC
from vaaibody.utilities.utils import angle_between_two_vectors

from vaaibody.core.blending import BlendingInertialization, JointBlendingInertialization
from vaaibody.core.database import (
    LatentFeatureDatabase,
    MotionAudioFeatureDatabase,
    MotionFeatureDatabase,
)
from vaaibody.core.motion import Motion
from vaaibody.core.skeleton import *


class GestureMatching(object):
    def __init__(
        self,
        gesture_db: MotionAudioFeatureDatabase,
        step_size=48,
        silent_db: Optional[MotionFeatureDatabase] = None,
        latent_db: Optional[LatentFeatureDatabase] = None,
        decompressor=None,
        decompressor_mean_out=None,
        decompressor_std_out=None,
    ):
        # neural network
        self.latent_db = latent_db

        self.decompressor = decompressor
        self.decompressor_mean_out = decompressor_mean_out
        self.decompressor_std_out = decompressor_std_out

        if self.decompressor is None:
            self.use_nn = False
        else:
            self.use_nn = True
            self.latent_feature = latent_db.latent_feature

        # db
        self._silent_db = silent_db
        self._gesture_db = gesture_db

        self.skeleton = self._gesture_db._skel
        self.frame_time = self._gesture_db._frame_time
        self.slice = self._gesture_db.slice

        self.n_db_motion = self._gesture_db._num_motion
        self.n_db_seq = self._gesture_db._num_seq
        self.n_db_frame = self._gesture_db._num_frame

        self.head_base = self._gesture_db.head_base
        self.step_size = step_size
        self.original_step_size = self.step_size

        # self.head_joint_matching = self._gesture_db._head_feature.matching
        self.head_joint_matching = MCS_SPINES

        # feature
        # self.pose_feat = []
        # self.mfcc_feat = []
        # self.beat_feat = []
        # self.lower_feat = []
        # self.head_feat = []
        # self.silent_release_feat = []
        # self.silent_head_feat = []

        # threshold
        self.is_speaking = True
        self.energy_term = 0.35
        self.thresh = 4.0
        self.angle_thresh_degree = 1000
        # self.thresh = 10
        self.max_onset = min(round(1.2 / self.frame_time), self.n_db_frame - 2)
        # self.max_onset = round(1. / self.frame_time)
        self.min_onset = round(0.25 / self.frame_time)

        # initialize
        self.tc = TC()
        self.init_feat()
        self.init_KD_tree()

    def reset(
        self,
    ):
        pass

    def init_feat(self):
        # feature
        self.pose_feature = self._gesture_db.pose_feature
        self.lower_feature = self._gesture_db.lower_feature
        self.head_feature = self._gesture_db.head_feature
        self.mfcc_feature = self._gesture_db.mfcc_feature
        self.beat_feature = self._gesture_db.beat_feature

        if self._silent_db is not None:
            self.silent_release_feature = self._silent_db.pose_feature
            self.silent_head_feature = self._silent_db.head_feature

        self.n_pose_feature = self._gesture_db._pose_feature_size
        self.n_lower_feature = self._gesture_db._lower_feature_size
        self.n_head_feature = self._gesture_db._head_feature_size
        self.n_mfcc_feature = self._gesture_db._mfcc_feature_size
        self.n_beat_feature = self._gesture_db._beat_feature_size

    def init_frame(self, is_rand: bool = True) -> Tuple[int, int, int]:
        """
        is_rand가 True일 경우 랜덤한 idx, 아닐 경우 0,0,0 반환
            motion: db 안에 motion idx
            seq: slice 되었을 경우에 idx
            frame idx와 seq frame을 합쳐서 motion 안에서 idx를 찾는다.
        """
        if is_rand:
            init_motion = np.random.randint(0, self.n_db_motion)
            if self.slice:
                init_seq = np.random.randint(0, self.n_db_seq[init_motion])
                init_frame = np.random.randint(0, self.n_db_frame)
            else:
                init_seq = np.random.randint(0, self.n_db_seq)
                init_frame = np.random.randint(0, self.n_db_frame[init_motion])
        else:
            init_motion = 0
            init_seq = 0
            init_frame = 0

        return init_motion, init_seq, init_frame

    def init_KD_tree(
        self,
    ):
        pose_feature = self.pose_feature
        lower_feature = self.lower_feature
        head_feature = self.head_feature
        n_head_feature = self.n_head_feature
        silent_release_feature = self.silent_release_feature

        self.KDtree_pose = []
        self.KDtree_lower = []
        self.KDtree_head = []
        for idx_motion in range(self.n_db_motion):
            motion_kd_tree = []
            motion_kd_tree_low = []
            motion_kd_tree_head = []
            for idx_seq in range(pose_feature[idx_motion].shape[0]):
                seq_kd_tree = KDTree(
                    pose_feature[idx_motion][idx_seq, :, :], metric="euclidean"
                )
                motion_kd_tree.append(seq_kd_tree)
                seq_low_tree = KDTree(
                    lower_feature[idx_motion][idx_seq, :, :], metric="euclidean"
                )
                motion_kd_tree_low.append(seq_low_tree)
                seq_head_tree = KDTree(
                    head_feature[idx_motion][idx_seq, :, :n_head_feature],
                    metric="euclidean",
                )
                motion_kd_tree_head.append(seq_head_tree)
            self.KDtree_pose.append(motion_kd_tree)
            self.KDtree_lower.append(motion_kd_tree_low)
            self.KDtree_head.append(motion_kd_tree_head)

        if self._silent_db is not None:
            self.KDtree_sil_rel = []
            for idx_motion in range(self._silent_db._num_motion):
                sil_rel_kd_tree = []
                for idx_seq in range(silent_release_feature[idx_motion].shape[0]):
                    seq_sil_rel_kd_tree = KDTree(
                        silent_release_feature[idx_motion][idx_seq, :, :],
                        metric="euclidean",
                    )
                    sil_rel_kd_tree.append(seq_sil_rel_kd_tree)
                self.KDtree_sil_rel.append(sil_rel_kd_tree)

    def verify_radius(
        self,
        index,
        feat,
    ):
        """
        radius
        """
        idx_motion, idx_seq, idx_frame = index
        adders = [0, self.step_size // 2, self.step_size - 1]
        for add in adders:
            cur_feature = feat[idx_motion][idx_seq, idx_frame + add, :3]
            base_root = (
                self.blended_frames[self.head_cnt + add]
                .get_global_rotation_by_name(self.head_base)
                .as_matrix()
            )
            rot_front = np.matmul(np.linalg.inv(base_root), cur_feature)
            ang = angle_between_two_vectors(rot_front, np.array([0, 0, 1]))
            if ang > self.angle_thresh_degree:
                return False
        return True

    def search_pose_cands_KD(
        self, body_test_feature: np.ndarray, max_query: int = 50
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Args:
            body_test_feature
            max_query :

        Returns:
            pose_dist_cands
            motion_cands
            pose_feature_cands
            mfcc_feature_cands
            beat_feature_cands
        """
        pose_dist_cands = []
        motion_cands = []
        pose_feature_cands = []
        mfcc_feature_cands = []
        beat_feature_cands = []
        body_test_feature = np.expand_dims(body_test_feature, axis=0)
        for idx_motion in range(self.n_db_motion):  # n_motion
            for idx_seq in range(self.pose_feature[idx_motion].shape[0]):  # n_seq
                current_KD = self.KDtree_pose[idx_motion][idx_seq]
                pose_cand_ctr = 0
                pose_cand_found = False
                dist, ind = current_KD.query(body_test_feature, k=max_query)
                while pose_cand_ctr < max_query:
                    idx_frame = ind[0][pose_cand_ctr]  # 한 시퀀스 안에 frame idx
                    d = dist[0][pose_cand_ctr]
                    pose_cand_ctr += 1
                    if d == 0.0:  # 지금 pose랑 완전히 같음
                        continue
                    if (
                        idx_frame >= self.n_db_frame - self.step_size
                    ):  # step size보다 남은 프레임이 적을 경우 쓰지 않음.
                        continue
                    if d > self.thresh:
                        break
                    else:
                        pose_cand_found = True
                        break

                if pose_cand_found == False:
                    continue
                """
                To make each feature shape to  the ((feature_size, step_size))
                """
                pose_feature_cand = self.pose_feature[idx_motion][
                    idx_seq, idx_frame : (idx_frame + self.step_size), :
                ].transpose()
                mfcc_feature_cand = self.mfcc_feature[idx_motion][
                    idx_seq, idx_frame : (idx_frame + self.step_size), :
                ].transpose()
                beat_feature_cand = self.beat_feature[idx_motion][
                    idx_seq, idx_frame : (idx_frame + self.step_size), :
                ].transpose()
                pose_dist_cands.append(d)
                motion_cands.append([idx_motion, idx_seq, idx_frame, self.step_size])
                pose_feature_cands.append(pose_feature_cand)
                mfcc_feature_cands.append(mfcc_feature_cand)
                beat_feature_cands.append(beat_feature_cand)

        pose_dist_cands = np.array(pose_dist_cands)
        motion_cands = np.array(motion_cands)
        pose_feature_cands = np.array(pose_feature_cands)
        mfcc_feature_cands = np.array(mfcc_feature_cands)
        beat_feature_cands = np.array(beat_feature_cands)

        return (
            pose_dist_cands,
            motion_cands,
            pose_feature_cands,
            mfcc_feature_cands,
            beat_feature_cands,
        )

    def search_motion_only_cands_KD(
        self,
        body_test_feature: np.ndarray,
        KD_type: str = "lower",
        max_query: int = 50,
        init_i: int = 0,
        init_k: int = 0,
    ):
        """
        Args:
            body_test_feature
            max_query

        Returns:
            pose_dist_cands
            motion_cands
            pose_feature_cands
        """
        pose_dist_cands = []
        motion_cands = []
        pose_feature_cands = []
        KD_now = None
        if KD_type == "lower":
            KD_now = self.KDtree_lower
            feat = self.lower_feature
        elif KD_type == "silent_rel":
            KD_now = self.KDtree_sil_rel
            feat = self.silent_release_feature
        elif KD_type == "head":
            KD_now = self.KDtree_head
            feat = self.head_feature

        body_test_feature = np.expand_dims(body_test_feature, axis=0)
        for idx_motion in range(len(KD_now)):
            for idx_seq in range(len(KD_now[idx_motion])):
                if KD_type == "lower":
                    if idx_motion == init_i and idx_seq == init_k:
                        continue
                current_KD = KD_now[idx_motion][idx_seq]
                pose_cand_ctr = 0
                pose_cand_found = False
                dist, ind = current_KD.query(body_test_feature, k=max_query)
                while pose_cand_ctr < max_query:
                    idx_frame = ind[0][pose_cand_ctr]
                    d = dist[0][pose_cand_ctr]
                    pose_cand_ctr += 1
                    if d == 0.0:
                        continue
                    if idx_frame >= feat[idx_motion].shape[1] - self.step_size:
                        continue
                    if KD_type == "head":
                        # To do: Implement the head range
                        if not self.verify_radius(
                            (idx_motion, idx_seq, idx_frame), feat
                        ):
                            continue
                    else:
                        if d > self.thresh:
                            break
                    pose_cand_found = True
                    break
                if pose_cand_found == False:
                    continue
                """
                To make each feature shape to  the ((feature_size, step_size))
                """
                pose_feature_cand = feat[idx_motion][
                    idx_seq, idx_frame : (idx_frame + self.step_size), :
                ].transpose()
                pose_dist_cands.append(d)
                motion_cands.append([idx_motion, idx_seq, idx_frame, self.step_size])
                pose_feature_cands.append(pose_feature_cand)
        pose_dist_cands = np.array(pose_dist_cands)
        motion_cands = np.array(motion_cands)
        pose_feature_cands = np.array(pose_feature_cands)
        return pose_dist_cands, motion_cands, pose_feature_cands


    def play_motion(self, lower_motion, lower_seq, lower_frm):
        play_list = []
        if lower_frm + self.step_size >= self.n_db_frame:
            for frm in range(lower_frm + 1, self.n_db_frame):
                play_list.append([lower_motion, lower_seq, frm])
            res = lower_frm + self.step_size - self.n_db_frame + 1
            if lower_seq + 1 < self.n_db_seq[lower_motion]:
                for i in range(res):
                    play_list.append([lower_motion, lower_seq + 1, i])
            else:
                l_feature = self.lower_feature[lower_motion][
                    lower_seq, self.n_db_frame - 1, :
                ].transpose()
                (
                    lower_dist_cands,
                    lower_motion_cands,
                    _,
                ) = self.search_motion_only_cands_KD(
                    l_feature, init_i=lower_motion, init_k=lower_seq
                )
                lower_score = np.array(lower_dist_cands).argsort().argsort()
                lower_sorted_list = np.argsort(lower_score).tolist()
                lower_motion_cands = lower_motion_cands[lower_sorted_list]
                motion, seq, frm, _ = lower_motion_cands[0]
                for i in range(res):
                    play_list.append([motion, seq, frm + i])
        else:
            for i in range(1, self.step_size + 1):
                play_list.append([lower_motion, lower_seq, lower_frm + i])

        return play_list


    def match_motion_with_silent(
        self,
        mfcc_test: np.ndarray,
        beat_test: np.ndarray,
        desired_k: int = 0,
        search_lower: bool = True,
        sil_hint: np.ndarray = None,
    ):
        """
        feature를 받아 모션을 검색하고, self.blend_frames에 결과를 저장함
        (이 값을 Motion Class로 반환하는 건 convert_frames 함수)

        Args:
            mfcc_test (n_feature, n_frame) - (420, n_frame)
            beat_test (n_feature, n_frame) - (60, n_frame)
            desired_k - mm 할 때 등수 매길 때 몇 번째 등수를 쓸 건지 결정. train 할 때 0~5까지 random 할수도 있음
            search_lower - lower body에 대해 play할지 search할 지
            sil_hint
        Returns:
            None
        """

        if self._silent_db is None:
            raise RuntimeError("Silent release DB must be given")

        self.silent = sil_hint
        n_frames = mfcc_test.shape[-1]
        """
        Here, the shape of test is ((n_feat, n_frm))
        """
        mfcc_test = np.concatenate(
            (mfcc_test[:, 0:1], mfcc_test), axis=1
        )  # 420, n_frame
        beat_test = np.concatenate(
            (beat_test[:, 0:1], beat_test), axis=1
        )  # 60, n_frame
        pose_test = np.zeros((self.n_pose_feature, mfcc_test.shape[1]))  # 216, n_frame
        lower_test = np.zeros(
            (self.n_lower_feature, mfcc_test.shape[1])
        )  # 192, n_frame

        init_motion, init_seq, init_frm = self.init_frame(is_rand=False)
        init_lower_motion, init_lower_seq, init_lower_frm = self.init_frame(
            is_rand=False
        )

        pose_test[:, 0] = self.pose_feature[init_motion][init_seq, init_frm, :]
        if search_lower:
            lower_test[:, 0] = self.lower_feature[init_lower_motion][
                init_lower_seq, init_lower_frm, :
            ]
        else:
            lower_motion = init_lower_motion
            lower_seq = init_lower_seq
            lower_frm = init_lower_frm
        self.pred_motion_idx = []
        self.pred_lower_idx = []

        j = 1  # 입력 audio에 대해 현재 찾은 idx+1. 0이 아니라 1인 이유는 처음에 concat한 이유랑 같음.
        loop_flag = True
        start_time = time.time()
        while loop_flag:
            if self.silent is None:
                self.step_size = self.slice_with_beat(beat_test, j)
            else:
                self.step_size = self.slice_with_beatNsil(beat_test, j)
            if j + self.step_size >= n_frames:
                self.step_size = n_frames - j - 1
                loop_flag = False
            if self.is_speaking:
                (
                    pose_dist_cands,
                    motion_cands,
                    pose_feature_cands,
                    mfcc_feature_cands,
                    beat_feature_cands,
                ) = self.search_pose_cands_KD(
                    pose_test[:, j - 1]
                )  # search pose from all # KD
            else:
                (
                    pose_dist_cands,
                    motion_cands,
                    pose_feature_cands,
                ) = self.search_motion_only_cands_KD(
                    pose_test[:, j - 1], KD_type="silent_rel", max_query=20
                )  # search pose from only motion (음성 없이)
            pose_score = np.array(pose_dist_cands).argsort().argsort()

            if self.is_speaking:
                mfcc_score = self.sort_cosine_dist(mfcc_feature_cands, mfcc_test[:, j])
                beat_score, _ = self.sort_hamming_dist(
                    beat_feature_cands, beat_test[:, j]
                )
            total_score = pose_score
            if self.is_speaking:
                total_score += mfcc_score
                total_score += beat_score
            total_sorted_list = np.argsort(total_score).tolist()

            pose_feature_cands = pose_feature_cands[total_sorted_list]
            motion_cands = motion_cands[total_sorted_list]  #

            if search_lower:
                """
                Search lower pose based on the pose difference
                """
                (
                    lower_dist_cands,
                    lower_motion_cands,
                    lower_cands,
                ) = self.search_motion_only_cands_KD(
                    lower_test[:, j - 1], init_i=lower_motion, init_k=lower_seq
                )
                lower_score = np.array(lower_dist_cands).argsort().argsort()
                lower_sorted_list = np.argsort(lower_score).tolist()
                lower_cands = lower_cands[lower_sorted_list]
                lower_motion_cands = lower_motion_cands[lower_sorted_list]
                des_low = desired_k + np.random.randint(0, 3)
                lower_test[:, j : (j + self.step_size)] = lower_cands[des_low]
                self.pred_lower_idx.append(lower_motion_cands[des_low])
                lower_motion = self.pred_lower_idx[-1][0]
                lower_seq = self.pred_lower_idx[-1][1]
                lower_frm = self.pred_lower_idx[-1][2]
            else:
                """
                Play mode
                """
                low_mo = self.play_motion(lower_motion, lower_seq, lower_frm)
                self.pred_lower_idx.append(low_mo)
                lower_motion = low_mo[-1][0]
                lower_seq = low_mo[-1][1]
                lower_frm = low_mo[-1][2]

            pose_test[:, j : (j + self.step_size)] = pose_feature_cands[desired_k]
            self.pred_motion_idx.append(
                [motion_cands[desired_k], self.is_speaking]
            )  # motion_cands[desired_k] 가 최종 결과물, is_speaking 까지 해서 db에서 찾아올 예정
            j += self.step_size
        print("Matching takes {}seconds".format(time.time() - start_time))
        start_blend = time.time()
        self.blend_matched(init_lower_motion, search_lower, apply_filter="lpf")
        print("Blending takes {}seconds".format(time.time() - start_blend))

    def blend_matched(
        self,
        init_lower_motion: int,
        search_lower: bool = False,
        apply_filter: str = None,
    ):
        """
        Args:
            init_lower_motion
            search_lower
            filter

        Returns:
            self.blended_frames
        """

        self.blended_frames = []
        blend_dur = 90
        root_offset = Transform(R.identity(), np.array([0, 0, 0]))
        prev_motion = init_lower_motion
        use_sil_real = False
        pred_lower_idx_list = self.pred_lower_idx
        blended_frames = self.blended_frames
        print("Blending process")

        for i, motion_idx in enumerate(tqdm(self.pred_motion_idx)):
            if len(motion_idx) == 2:
                use_sil_real = True
                is_speaking = motion_idx[1]
                motion_idx = motion_idx[0]
            if search_lower:
                lower_idx = pred_lower_idx_list[i]
            else:
                lower_list = pred_lower_idx_list[i]
            if i > 0:
                first_motion, second_motion = (
                    blended_frames[-2],
                    self.blended_frames[-1],
                )
                if use_sil_real and not is_speaking:
                    target_frame = self._silent_db.get_sliced_frame(
                        motion_idx[0], motion_idx[1], motion_idx[2]
                    ).copy()
                else:
                    if self.use_nn:
                        target_frame = self._gesture_db.get_sliced_frame(
                            motion_idx[0], motion_idx[1], motion_idx[2]
                        ).copy()
                    else:
                        target_frame = self._gesture_db.get_aug_sliced_frame(
                            motion_idx[0], motion_idx[1], motion_idx[2]
                        ).copy()
                # Implement add lower body to the target frame
                if not search_lower:
                    lower_idx = lower_list[0]

                if self.use_nn:
                    target_lower = self._gesture_db.get_sliced_frame(
                        lower_idx[0], lower_idx[1], lower_idx[2]
                    )
                else:
                    target_lower = self._gesture_db.get_aug_sliced_frame(
                        lower_idx[0], lower_idx[1], lower_idx[2]
                    )

                target_frame.set_root_transform(target_lower.get_root_transform())
                for lower in self._gesture_db.lower_joints_matching:
                    low_tar = target_lower.get_local_rotation_by_name(lower)
                    target_frame.set_local_rotation_by_name(lower, low_tar)
                new_root = target_frame.get_root_transform()
                current_root = second_motion.get_root_transform()
                root_offset = current_root * new_root.inverse()
                target_frame.set_root_transform(
                    root_offset * target_frame.get_root_transform()
                )
                blender = BlendingInertialization(
                    second_motion,
                    first_motion,
                    target_frame,
                    blend_dur,
                    self.frame_time,
                    is_frame=True,
                )
                # blender =  JointBlendingInertialization("Neck", second_motion, first_motion, target_frame, blend_dur, self.frame_time)
            for step_size in range(
                motion_idx[3]
            ):  # modion_cand - i, k, f, self.step_size
                if use_sil_real and not is_speaking:
                    current_frame = self._silent_db.get_sliced_frame(
                        motion_idx[0], motion_idx[1], motion_idx[2] + step_size
                    ).copy()  # copy~
                else:
                    # TODO
                    if self.use_nn:
                        current_frame = self.get_sliced_frame_nn(
                            motion_idx[0],
                            motion_idx[1],
                            motion_idx[2] + step_size,
                        ).copy()
                    else:
                        current_frame = self._gesture_db.get_aug_sliced_frame(
                            motion_idx[0], motion_idx[1], motion_idx[2] + step_size
                        ).copy()

                # Implement add lower body to the target frame
                if not search_lower:
                    lower_idx = lower_list[step_size]
                    if self.use_nn:
                        target_lower = self._gesture_db.get_sliced_frame(
                            lower_idx[0], lower_idx[1], lower_idx[2]
                        )
                    else:
                        target_lower = self._gesture_db.get_aug_sliced_frame(
                            lower_idx[0], lower_idx[1], lower_idx[2]
                        )
                    if lower_idx[0] != prev_motion:
                        new_root = target_lower.get_root_transform()
                        current_root = self.blended_frames[-1].get_root_transform()
                        root_offset = current_root * new_root.inverse()
                        prev_motion = lower_idx[0]
                else:
                    if self.use_nn:
                        target_lower = self._gesture_db.get_sliced_frame(
                            lower_idx[0], lower_idx[1], lower_idx[2] + step_size
                        )
                    else:
                        target_lower = self._gesture_db.get_aug_sliced_frame(
                            lower_idx[0], lower_idx[1], lower_idx[2] + step_size
                        )
                # 하반신 덮어쓰기. 안그러면 발 미끌림
                current_frame.set_root_transform(
                    target_lower.get_root_transform()
                )  # lower body의 root를 따르겠음
                for lower in self._gesture_db.lower_joints_matching:  # 하반신 joint면
                    low_tar = target_lower.get_local_rotation_by_name(lower)
                    current_frame.set_local_rotation_by_name(
                        lower, low_tar
                    )  # local rotation == joint angle
                if i > 0 and step_size < blend_dur:
                    current_frame = blender.apply_frame_blending(
                        current_frame, step_size + 1
                    )
                self.blended_frames.append(current_frame)
        if apply_filter is not None:
            self.blended_frames = filter_frames(self.blended_frames, apply_filter)
        return self.blended_frames

    def matching_head(self, filter=None):
        """
        motion_idx 수정 필요
        """
        # To do : Matching algorithm
        print("Matching head")
        is_filter = False
        if filter is not None:
            is_filter = True
        blend_dur = 90
        self.head_cnt = 0
        head_test = np.zeros((self.n_head_feature, len(self.blended_frames)))
        init_motion_idx = self.pred_motion_idx[0]
        if len(init_motion_idx) == 2:
            init_motion_idx = init_motion_idx[0]
            is_speaking = init_motion_idx[1]
        if is_speaking:
            head_test[:, 0] = self.head_feature[init_motion_idx[0]][
                init_motion_idx[1], init_motion_idx[2], :
            ]
        else:
            head_test[:, 0] = self.silent_head_feature[init_motion_idx[0]][
                init_motion_idx[1], init_motion_idx[2], :
            ]
        for i, motion_idx in enumerate(tqdm(self.pred_motion_idx)):
            if len(motion_idx) == 2:
                motion_idx = motion_idx[0]
            self.step_size = motion_idx[3]
            (
                head_dist_cands,
                head_motion_cands,
                head_cands,
            ) = self.search_motion_only_cands_KD(
                head_test[:, max(self.head_cnt - 1, 0)], KD_type="head", max_query=100
            )
            head_score = np.array(head_dist_cands).argsort().argsort()
            head_sorted_list = np.argsort(head_score).tolist()
            head_cands = head_cands[head_sorted_list]
            head_motion_cands = head_motion_cands[head_sorted_list]
            head_test[:, self.head_cnt : (self.head_cnt + self.step_size)] = head_cands[
                0
            ]
            head_idx = head_motion_cands[0]
            if i > 0:
                first_motion = self.blended_frames[self.head_cnt - 2]
                second_motion = self.blended_frames[self.head_cnt - 1]
                if self.use_nn:
                    target_frame = self._gesture_db.get_sliced_frame(
                        head_idx[0], head_idx[1], head_idx[2]
                    ).copy()
                else:
                    target_frame = self._gesture_db.get_aug_sliced_frame(
                        head_idx[0], head_idx[1], head_idx[2]
                    ).copy()
                match_flag = False
                blenders = {}
                for joint_name in self.head_joint_matching:
                    if joint_name == self.head_base:
                        match_flag = True
                    if match_flag:
                        blenders[joint_name] = JointBlendingInertialization(
                            joint_name,
                            second_motion,
                            first_motion,
                            target_frame,
                            blend_dur,
                            self.frame_time,
                        )

            for step_size in range(self.step_size):
                current_frame = self.blended_frames[self.head_cnt + step_size]
                match_flag = False
                for joint_name in self.head_joint_matching:
                    if joint_name == self.head_base:
                        match_flag = True
                    if match_flag:
                        if self.use_nn:
                            target_head = self._gesture_db.get_sliced_frame(
                                head_idx[0], head_idx[1], head_idx[2] + step_size
                            ).copy()
                        else:
                            target_head = self._gesture_db.get_aug_sliced_frame(
                                head_idx[0], head_idx[1], head_idx[2] + step_size
                            ).copy()

                        head_tar = target_head.get_local_rotation_by_name(joint_name)
                        current_frame.set_local_rotation_by_name(joint_name, head_tar)
                        start_time = time.time()
                        if i > 0 and step_size < blend_dur:
                            current_frame = blenders[joint_name].apply_frame_blending(
                                current_frame, step_size + 1
                            )
            self.head_cnt += self.step_size
        if is_filter:
            self.blended_frames = filter_frames(self.blended_frames, filter)

    def convert_frames(
        self,
    ):
        self.matched = Motion(self.skeleton, self.blended_frames, self.frame_time)
        return self.matched

    def slice_with_beat(self, beat_test: np.ndarray, j: int) -> int:
        end_point = min(beat_test.shape[1] - 1, j + self.max_onset)
        for i in range(j + self.min_onset, end_point):
            if beat_test[0, i] == 1:
                return i - j
        return end_point - j

    def slice_with_beatNsil(self, beat_test: np.ndarray, j: int) -> int:
        end_point = min(beat_test.shape[1], j + self.max_onset)
        if self.silent[j - 1] == 1:
            self.is_speaking = False
            for i in range(j + 1, end_point):
                if self.silent[i - 1] == 0:
                    return i - j
            return end_point - j
        else:
            self.is_speaking = True
            for i in range(j + 1, end_point):
                if self.silent[i - 1] == 1:
                    return i - j
                if i >= j + self.min_onset and beat_test[0, i] == 1:
                    return i - j
            return end_point - j

    def sort_hamming_dist(self, src, dist):
        ham_dist = []
        for k in range(src.shape[0]):
            ham_score = spatial.distance.hamming(src[k, :, 0], dist)
            ham_dist.append(ham_score)
        return np.array(ham_dist).argsort().argsort(), ham_dist

    def sort_cosine_dist(self, src: np.ndarray, dist: np.ndarray) -> np.ndarray:
        cos_dist = []
        for k in range(src.shape[0]):
            if np.linalg.norm(src[k, :, 0]) < 1e-8:
                src[k, :, 0] = np.ones_like(src[k, :, 0]) * 1e-8
            if np.linalg.norm(dist) < 1e-8:
                dist = np.ones_like(dist) * 1e-8
            audio_sim_score = spatial.distance.cosine(src[k, :, 0], dist)
            # audio_sim_score += self.energy_term * pow((src[k,-1,0] - dist[-1]), 2)
            cos_dist.append(audio_sim_score)
        return np.array(cos_dist).argsort().argsort()

    def sort_euclidean_dist(self, src, dist):
        pass

    def get_sliced_frame_nn(self, idx_motion: int, idx_seq: int, idx_frame: int):
        """
        return Frame
        """
        pose_feature = self.pose_feature[idx_motion][idx_seq][idx_frame]
        latent_feature = self.latent_feature[idx_motion][idx_seq][idx_frame]

        import torch

        with torch.no_grad():
            pose_feature = torch.as_tensor(pose_feature).to(torch.float32)  # 513
            latent_feature = torch.as_tensor(latent_feature).to(torch.float32)  # 64

            # batch, window, n_feature
            Ytil = (
                self.decompressor(
                    torch.cat([pose_feature, latent_feature], dim=-1).reshape(1, 1, -1)
                )
                * self.decompressor_std_out
                + self.decompressor_mean_out
            )

            n_joint = 61
            Ytil_pos = Ytil[:, :, 0 * (n_joint - 1) : 3 * (n_joint - 1)].reshape(
                [1, 1, n_joint - 1, 3]
            )
            Ytil_txy = Ytil[:, :, 3 * (n_joint - 1) : 9 * (n_joint - 1)].reshape(
                [1, 1, n_joint - 1, 3, 2]
            )

            # Ytil_rvel = Ytil[
            #     :, :, 15 * (n_joint - 1) + 0 : 15 * (n_joint - 1) + 3
            # ].reshape([1, stop - start, 3])
            # Ytil_rang = Ytil[
            #     :, :, 15 * (n_joint - 1) + 3 : 15 * (n_joint - 1) + 6
            # ].reshape([1, stop - start, 3])

            # Convert to quat and remove batch

            Ytil_rot = quat.from_xform_xy(Ytil_txy[0].cpu().numpy())
            Ytil_pos = Ytil_pos[0].cpu().numpy()
            # Ytil_rvel = Ytil_rvel[0].cpu().numpy()
            # Ytil_rang = Ytil_rang[0].cpu().numpy()

            # Ytil_rot = np.concatenate([R.random(1).as_quat().reshape(1,1,4), Ytil_rot], axis=1)
            # Ytil_pos = np.concatenate([np.ones((1, 1, 3)), Ytil_pos], axis=1)

            root_rot = np.array([-0.0321, -0.6754, -0.0286, 0.7362]).reshape(1, 1, 4)
            root_pos = np.array([-6.9389e-17, 9.6884e-01, 8.1532e-17]).reshape(1, 1, 3)

            Ytil_rot = np.concatenate([root_rot, Ytil_rot], axis=1)  # pad
            Ytil_pos = np.concatenate([root_pos, Ytil_pos], axis=1)

            local_transforms_til = get_local_transform_from_posrot(Ytil_pos, Ytil_rot)
            cur_frame = Frame(
                self.skeleton, local_transforms_til[0][0], local_transforms_til[0]
            )
        return cur_frame
