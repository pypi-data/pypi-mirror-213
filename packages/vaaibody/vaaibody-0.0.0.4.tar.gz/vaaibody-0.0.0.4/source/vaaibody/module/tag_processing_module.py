from collections import deque
import pandas as pd
import numpy as np
import string
from core.frame import Frame
from utilities.frame_utils import find_single_cut_idx
from utilities.timechecker import TimeChecker as TC


class PhaseInformation:
    def __init__(self, db, phase_file) -> None:
        self.phase_info = pd.read_csv(phase_file)
        self.idx_phase_list = []
        self.tag_names = []
        self.motion = {}
        self.tag = {}
        self.phase = {}
        self.phase_names = ["Stroke", "Hold", "Retract", "End"]
        for file_name in self.phase_info["File"]:
            current_info = self.phase_info.loc[self.phase_info["File"] == file_name]
            idx_phase, phase_motion = db.get_idx_motion_by_name(file_name)
            current_tag = current_info["Tag"].iloc[0]
            self.idx_phase_list.append(idx_phase)
            self.motion[idx_phase] = phase_motion
            self.tag[idx_phase] = current_info["Tag"].iloc[0]
            phase_dict = {}
            for name in self.phase_names:
                phase_dict[name] = int(current_info[name].iloc[0])
            self.phase[idx_phase] = phase_dict
            if current_tag not in self.tag_names:
                self.tag_names.append(current_tag)

    def get_motion(self, idx_phase):
        return self.motion[idx_phase]

    def get_tag(self, idx_phase):
        return self.tag[idx_phase]

    def get_phase(self, idx_phase, phase_name):
        if phase_name not in self.phase_names:
            raise Exception("Not a valid phase")
        current_phase_dict = self.phase[idx_phase]
        return current_phase_dict[phase_name]


class TagProcessingModule(object):
    def __init__(self, db, phase_file, pose_feature, feature_db) -> None:
        """
        Funtion:
            phase information 읽어온다.
        """
        self.pose_feature = pose_feature
        self.feature_db = feature_db
        self.phase_info = PhaseInformation(db, phase_file)
        self.tag_list = self.phase_info.tag_names
        self.loop_motion = []
        self.numpy_feature_db, self.idx_list = self.feature_db.numpy_db()

    def reset(
        self,
    ):
        self.idx_loop_start = -1
        self.idx_retract_start = -1
        self.loop_len = 1
        self.loop_motion = []
        self.hold_end = 0

    def search_tagged_motion(
        self,
        motion_future: deque,
        motion_tag: string = "Untagged",
        start_feature="Stroke",
        end_feature="Hold",
        blend_duration=30,
    ):
        """
        Args
            motion_future
            motion_tag
            start_feature
            end_feature

        Returns
            찾은 tagged motion 에 대한 정보들
        """

        current_motion_feature = (
            self.pose_feature.compute_single_frame_feature_from_frame(motion_future)
        )
        min_cost = 1e10
        for idx_motion in self.phase_info.idx_phase_list:
            if motion_tag != "Untagged" and motion_tag != self.phase_info.get_tag(
                idx_motion
            ):
                continue

            feat_start = self.phase_info.get_phase(idx_motion, start_feature)
            feat_end = self.phase_info.get_phase(idx_motion, end_feature)
            if end_feature == "End":
                feat_end -= blend_duration
            target_motion_feature = self.feature_db._gesture_feature_DB[idx_motion][0][
                0
            ]
            idx_frm, cost = find_single_cut_idx(
                current_motion_feature,
                target_motion_feature,
                idx_feat_start=feat_start,
                idx_feat_end=feat_end,
            )
            if cost < min_cost:
                back_feat_hold = self.phase_info.get_phase(idx_motion, "Hold")
                back_feat_retract = self.phase_info.get_phase(idx_motion, "Retract")
                holding_time = back_feat_retract - back_feat_hold
                min_cost = cost
                back_frame_candidate = idx_frm
                back_motion_candidate = idx_motion
        return (
            back_motion_candidate,
            back_frame_candidate,
            back_feat_hold,
            back_feat_retract,
            holding_time,
        )

    def process_matching_profile(
        self,
        back_motion_candidate,
        back_frame_candidate,
        back_feat_hold,
        back_feat_retract,
        holding_time,
        blend_duration: int,
        duration_tag: int = -1,
    ):
        """
        찾은 tagged motion의 정보들과 duration tag를 이용하여
        Transition과 관련한 변수들을 계산
            - moving inertialization 여부
            - duration tag 대응
            -
        """
        if back_frame_candidate >= back_feat_retract:
            moving_blend_flag = True
        elif back_feat_hold > back_frame_candidate + blend_duration:
            moving_blend_flag = True
        else:
            moving_blend_flag = False

        if duration_tag > 0:
            hold_st = back_feat_hold - back_frame_candidate
            if moving_blend_flag:
                hold_st += blend_duration
            self.hold_end = hold_st + duration_tag
            self.idx_retract_start = self.phase_info.get_phase(
                back_motion_candidate, "Retract"
            )
            if holding_time < duration_tag:
                loop_motion_feature = self.feature_db._gesture_feature_DB[
                    back_motion_candidate
                ][0][0]
                idx_start = self.phase_info.get_phase(back_motion_candidate, "Hold")
                self.idx_loop_start, _ = find_single_cut_idx(
                    loop_motion_feature[self.idx_retract_start - 1],
                    loop_motion_feature,
                    idx_feat_start=idx_start,
                    idx_feat_end=idx_start
                    + (self.idx_retract_start - idx_start - 1) // 4,
                )
                self.loop_len = self.idx_retract_start - self.idx_loop_start
        else:
            self.hold_end = back_feat_retract
            if moving_blend_flag:
                self.hold_end += blend_duration
        return (
            self.phase_info.get_motion(back_motion_candidate),
            back_frame_candidate,
            moving_blend_flag,
        )

    def feature_masking_tag_feature(
        self,
        motion_tag: string,
        start_feature: string,
        end_feature: string,
        blend_duration,
    ):
        """
        이 방법이 더 느려서 사용하지 않음
        나중에 비슷한 아이디어가 있을 수 있어서 코드는 남겨 둠
        """
        masked_feature = np.ones_like(self.numpy_feature_db) * 1000000
        for idx_motion in self.phase_info.idx_phase_list:
            idx_start = self.idx_list[idx_motion]
            if motion_tag != "Untagged" and motion_tag != self.phase_info.get_tag(
                idx_motion
            ):
                continue
            feat_start = self.phase_info.get_phase(idx_motion, start_feature)
            feat_end = self.phase_info.get_phase(idx_motion, end_feature)
            if end_feature == "End":
                feat_end -= blend_duration
            if feat_start >= feat_end:
                continue
            masked_feature[
                idx_start + feat_start : idx_start + feat_end
            ] = self.numpy_feature_db[idx_start + feat_start : idx_start + feat_end]
        return masked_feature
