from collections import deque

import numpy as np
from parameter.gesture_matching_parameter import (MCS_LOWER,
                                                  MCS_LOWER_BLENDING, MCS_NON,
                                                  MCS_SPINES, MCS_UPPER,
                                                  MCS_UPPER_2)
from utilities.frame_utils import get_position_vel

""""
Here, we define the pose feature and the audio feature
We first define the upper body pose feature and then move on to the full body
The upper body pose features are the relative positions of below body parts to the root.
- Both side elbow, wrist, index_base, little_base. (Total 8 joints)
"""


class JointFeature:
    def __init__(
        self, joints, weight: float = 1.0, min_cost: float = 0.0, max_cost=None
    ):
        self._joints = joints
        self._weight = weight
        self._min_cost = min_cost  # lower than min cost is set to min cost
        self._max_cost = (
            max_cost  # if not None, feature vector with higher cost is pruned
        )
        self._dof = self.compute_dof()

    @property
    def dof(self):
        return self._dof

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    @property
    def min_cost(self):
        return self._min_cost

    @property
    def max_cost(self):
        return self._max_cost

    def compute_dof(self):
        return NotImplementedError()

    def compute_feature(self, prev_pose, pose):
        return NotImplementedError()

    def compute_feature(self, motion):
        return NotImplementedError()


class AudioFeature:
    def __init__(
        self,
        beat_look_ahead: list = range(15),
        beat_look_behind: list = [],
        aud_feat_idx: list = [0, 2, 4, 8, 10, 12, 14],
        ncep=13,
    ):
        self._beat_look_ahead = beat_look_ahead
        self._beat_look_behind = beat_look_behind
        self._aud_feat_idx = aud_feat_idx
        self._ncep = ncep
        self._beat_dof = self.compute_beat_dof()
        self._mfcc_dof = self.compute_mfcc_dof()

    @property
    def beat_dof(self):
        return self._beat_dof

    @property
    def mfcc_dof(self):
        return self._mfcc_dof

    def compute_beat_dof(self):
        return len(self._beat_look_ahead) + len(self._beat_look_behind)

    def compute_mfcc_dof(
        self,
    ):
        return len(self._aud_feat_idx) * (self._ncep + 1)

    def compute_mfcc_feature(self, mfcc):
        mfcc_feature = np.zeros(
            (mfcc.shape[0], len(self._aud_feat_idx), self._ncep + 1)
        )
        for i, idx in enumerate(self._aud_feat_idx):
            post_pad = np.zeros((idx, self._ncep + 1))
            mfcc_feature[:, i, :] = np.concatenate((mfcc[idx:, :], post_pad), axis=0)
        mfcc_feature = mfcc_feature.reshape((mfcc.shape[0], -1))
        return mfcc_feature

    def compute_mfcc_feature_der(
        self,
    ):
        pass

    def compute_beat_feature(self, beat):
        beat_feature = np.zeros((beat.shape[0], self._beat_dof, 1))
        for i, idx in enumerate(self._beat_look_behind):
            pre_pad = np.zeros((idx, 1))
            beat_feature[:, i, :] = np.concatenate(
                (pre_pad, beat_feature[:-idx, :]), axis=0
            )
        for i, idx in enumerate(self._beat_look_ahead):
            post_pad = np.zeros((idx, 1))
            beat_feature[:, i + len(self._beat_look_behind), :] = np.concatenate(
                (beat[idx:, :], post_pad), axis=0
            )
        beat_feature = beat_feature.reshape((beat.shape[0], -1))
        return beat_feature


class HeadPoseFeature:
    def __init__(
        self,
        look_ahead: list = [0],
        weight: float = 1,
        min_cost: float = 0,
        max_cost=None,
    ):
        # For talking hand data
        self._head_joint = "Head"
        self._base_joint = "Neck"
        self._matching = MCS_SPINES
        self._look_ahead = look_ahead
        self._dof = self.compute_dof()

    def compute_dof(
        self,
    ):
        return len(self._look_ahead) * 3

    @property
    def dof(self):
        return self._dof

    @property
    def head_joint(self):
        return self._head_joint

    @property
    def base_joint(self):
        return self._base_joint

    @property
    def matching(self):
        return self._matching

    # Depricated
    def get_inv_root_orientation(self, current_frame):
        rot_vec = current_frame.get_inverse_root_transform().rotation.as_rotvec()
        return rot_vec

    def get_component_head_feature(self, current_frame):
        global_direction = np.matmul(
            current_frame.get_global_transform_by_name(self._head_joint).rotation_np,
            np.array([0, 0, 1]),
        )
        return np.matmul(
            current_frame.get_global_transform_by_name(self._base_joint).rotation_np,
            global_direction,
        )

    def compute_feature(self, motion):
        m_num = motion.num_frame()
        single_feat = np.zeros((m_num, 3))
        for i in range(m_num):
            single_feat[i, :3] = self.get_component_head_feature(motion[i])
        body_feat = np.zeros((m_num, len(self._look_ahead), 3))
        for i, idx in enumerate(self._look_ahead):
            post_pad = np.zeros((idx, 3))
            body_feat[:, i, :] = np.concatenate(
                (single_feat[idx:, :], post_pad), axis=0
            )
        body_feat = body_feat.reshape((m_num, -1))
        return body_feat

class WeightedUpperPoseFeature(JointFeature):
    def __init__(
        self,
        look_ahead: list = [0],
        weight: float = 1,
        min_cost: float = 0,
        max_cost=None,
        gamma=0.5,
        decay=False,
    ):
        # For talking hand data
        self.joints = MCS_UPPER_2
        self._look_ahead = look_ahead
        self.gamma = gamma
        self.decay = decay
        super().__init__(self.joints, weight, min_cost, max_cost)

    def compute_dof(self):
        return len(self._joints) * len(self._look_ahead) * 3

    def compute_feature(self, motion):
        frame_num = motion.num_frame()
        single_feat = np.zeros((frame_num, len(self._joints) * 3))
        for idx_frame in range(frame_num):
            single_feat[idx_frame, :] = np.concatenate(
                [
                    motion._frames[idx_frame]
                    .get_component_transform_by_name(idx_joint)
                    .translation
                    for idx_joint in self._joints
                ],
                axis=-1,
            )
        body_feat = np.zeros((frame_num, len(self._look_ahead), len(self._joints) * 3))
        for idx, look_value in enumerate(self._look_ahead):
            post_pad = np.zeros((look_value, len(self._joints) * 3))
            if self.decay:
                body_feat[:, idx, :] = (self.gamma**idx) * np.concatenate(
                    (single_feat[look_value:, :], post_pad), axis=0
                )
            else:
                if idx > 0:
                    body_feat[:, idx, :] = self.gamma * np.concatenate(
                        (single_feat[look_value:, :], post_pad), axis=0
                    )
                else:
                    body_feat[:, idx, :] = np.concatenate(
                        (single_feat[look_value:, :], post_pad), axis=0
                    )
        body_feat = body_feat.reshape((frame_num, -1))
        return body_feat


class WeightedUpperVelFeature(JointFeature):
    def __init__(
        self,
        look_ahead: list = [0],
        weight: float = 1,
        min_cost: float = 0,
        max_cost=None,
        gamma=0.5,
        decay=False,
    ):
        # For talking hand data
        self.joints = MCS_UPPER
        self._look_ahead = look_ahead
        self.gamma = gamma
        self.decay = decay
        super().__init__(self.joints, weight, min_cost, max_cost)

    def compute_dof(self):
        return len(self._joints) * (len(self._look_ahead) + 1) * 3

    def compute_feature(self, motion):
        joint_dict = motion._skeleton.joint_dict
        frame_num = motion.num_frame()
        vel_motion = get_position_vel(motion)
        single_feat = np.zeros((frame_num, len(self._joints) * 3))
        vel_feat = np.zeros((frame_num, len(self._joints) * 3))
        for idx_frame in range(frame_num):
            single_feat[idx_frame, :] = np.concatenate(
                [
                    motion._frames[idx_frame]
                    .get_component_transform_by_name(idx_joint)
                    .translation
                    for idx_joint in self._joints
                ],
                axis=-1,
            )
            vel_feat[idx_frame, :] = np.concatenate(
                [
                    vel_motion[idx_frame, 3 * joint_dict[j] : 3 * (joint_dict[j] + 1)]
                    for j in self._joints
                ],
                axis=-1,
            )
        body_feat = np.zeros(
            (frame_num, len(self._look_ahead) + 1, len(self._joints) * 3)
        )
        for i, idx in enumerate(self._look_ahead):
            post_pad = np.zeros((idx, len(self._joints) * 3))
            if self.decay:
                body_feat[:, i, :] = (self.gamma**i) * np.concatenate(
                    (single_feat[idx:, :], post_pad), axis=0
                )
            else:
                if i > 0:
                    body_feat[:, i, :] = self.gamma * np.concatenate(
                        (single_feat[idx:, :], post_pad), axis=0
                    )
                else:
                    body_feat[:, i, :] = np.concatenate(
                        (single_feat[idx:, :], post_pad), axis=0
                    )
        body_feat[:, -1, :] = vel_feat
        body_feat = body_feat.reshape((frame_num, -1))
        return body_feat


class LowerPoseFeature(JointFeature):
    def __init__(
        self,
        look_ahead: list = [0],
        weight: float = 1,
        min_cost: float = 0,
        max_cost=None,
    ):
        self.joints = MCS_LOWER
        self.joints_matching = MCS_LOWER_BLENDING
        self._look_ahead = look_ahead
        super().__init__(self.joints, weight, min_cost, max_cost)

    def compute_dof(self):
        return len(self._joints) * len(self._look_ahead) * 3

    def compute_feature(self, motion):
        m_num = motion.num_frame()
        single_feat = np.zeros((m_num, len(self._joints) * 3))
        for idx_frame in range(m_num):
            single_feat[idx_frame, :] = np.concatenate(
                [
                    motion._frames[idx_frame].get_component_transform_by_name(j).translation
                    for j in self._joints
                ],
                axis=-1,
            )
        body_feat = np.zeros((m_num, len(self._look_ahead), len(self._joints) * 3))
        for i, idx in enumerate(self._look_ahead):
            post_pad = np.zeros((idx, len(self._joints) * 3))
            body_feat[:, i, :] = np.concatenate(
                (single_feat[idx:, :], post_pad), axis=0
            )
        body_feat = body_feat.reshape((m_num, -1))
        return body_feat

class NonTalkingPoseFeature(JointFeature):
    def __init__(
        self,
        look_ahead: list = [0],
        weight: float = 1,
        min_cost: float = 0,
        max_cost=None,
    ):
        self.joints = MCS_NON
        self._look_ahead = look_ahead
        super().__init__(self.joints, weight, min_cost, max_cost)

    def update_look_ahead(self, look_ahead):
        self._look_ahead = look_ahead

    def compute_dof(self):
        return len(self._joints) * len(self._look_ahead) * 3

    def compute_feature(self, motion):
        joint_dict = motion._skeleton.joint_dict
        m_num = motion.num_frame()
        single_feat = np.zeros((m_num, len(self._joints) * 3))
        for idx_frame in range(m_num):
            single_feat[idx_frame, :] = np.concatenate(
                [
                    motion._frames[idx_frame].get_component_transform_by_name(j).translation
                    for j in self._joints
                ],
                axis=-1,
            )
        body_feat = np.zeros((m_num, len(self._look_ahead), len(self._joints) * 3))
        for i, idx in enumerate(self._look_ahead):
            post_pad = np.zeros((idx, len(self._joints) * 3))
            body_feat[:, i, :] = np.concatenate(
                (single_feat[idx:, :], post_pad), axis=0
            )
        body_feat = body_feat.reshape((m_num, -1))
        return body_feat

    def compute_single_frame_feature_from_motion(self, motion, desired_idx: int):
        m_num = len(self._look_ahead)
        single_feat = np.zeros((m_num, len(self._joints) * 3))
        for i, idx in enumerate(self._look_ahead):
            if desired_idx + idx >= motion.num_frame():
                single_feat[i, :] = np.zeros(len(self._joints) * 3)
            else:
                single_feat[i, :] = np.concatenate(
                    [
                        motion._frames[desired_idx + idx]
                        .get_component_transform_by_name(j)
                        .translation
                        for j in self._joints
                    ],
                    axis=-1,
                )
        body_feat = single_feat.reshape(m_num * len(self._joints) * 3)
        return body_feat

    def compute_single_frame_feature_from_frame(self, motion_deque: deque):
        m_num = len(self._look_ahead)
        single_feat = np.zeros((m_num, len(self._joints) * 3))
        for motion_index in range(m_num):
            frame = motion_deque.popleft()
            single_feat[motion_index, :] = np.concatenate(
                [
                    frame.get_component_transform_by_name(j).translation
                    for j in self._joints
                ],
                axis=-1,
            )
        body_feat = single_feat.reshape(m_num * len(self._joints) * 3)
        return body_feat

    def compute_cost(self, query, candidates):
        costs = np.sqrt((query - candidates) ** 2).mean(axis=-1)

        if self._max_cost is not None:
            available = costs < self._max_cost
        else:
            available = np.array([True] * candidates.shape[0])
        costs[costs < self._min_cost] = self._min_cost
        costs *= self._weight

        return available, costs


class NonTalkingHistoryFeature(JointFeature):
    def __init__(
        self,
        look_behind: list = [0],
        weight: float = 1,
        min_cost: float = 0,
        max_cost=None,
    ):
        self.joints = MCS_NON
        self._look_behind = look_behind
        super().__init__(self.joints, weight, min_cost, max_cost)

    def update_look_behind(self, look_behind):
        self._look_behind= look_behind

    def compute_dof(self):
        return len(self._joints) * len(self._look_behind) * 3

    def compute_feature(self, motion):
        m_num = motion.num_frame()
        single_feat = np.zeros((m_num, len(self._joints) * 3))

        """
        single feature 계산 부분
        """
        for i in range(m_num):
            single_feat[i, :] = np.concatenate(
                [
                    motion._frames[i].get_component_transform_by_name(j).translation
                    for j in self._joints
                ],
                axis=-1,
            )
        body_feat = np.zeros((m_num, len(self._look_behind), len(self._joints) * 3))
        
        """
        이 부분이 history로 패딩하는 코드이다.
        """
        for i, idx in enumerate(self._look_behind):
            if idx == 0:
                body_feat[:, i, :] = single_feat
                continue
            pre_pad = np.ones((idx, len(self._joints) * 3))
            pre_pad *= single_feat[0]
            body_feat[:, i, :] = np.concatenate(
                (pre_pad, single_feat[:-idx, :]), axis=0
            )
        body_feat = body_feat.reshape((m_num, -1))
        return body_feat
