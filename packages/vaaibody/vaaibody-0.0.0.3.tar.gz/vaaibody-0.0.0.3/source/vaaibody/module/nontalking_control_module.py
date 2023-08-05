from collections import deque
import numpy as np
import string
from core.database import MotionDatabase, DefaultMotionFeatureDatabase
from core.skeleton import Transform
from core.frame import Frame
from core.feature import NonTalkingPoseFeature, NonTalkingHistoryFeature
from module.idle_module import IdleModule
from module.transition_module import TransitionModule
from module.tag_processing_module import TagProcessingModule
from utilities.timechecker import TimeChecker as TC
from utilities.frame_utils import shift_root, find_single_cut_idx


class NonTalkingModule(object):
    def __init__(
        self,
        db: MotionDatabase,
        idle_file="./data/idle_HSO.csv",
        phase_file="./data/phase_HSO.csv",
        feature_path="./data/matching_data/",
        feature_file_name="HSO_convAI.pickle",
    ):
        """
        Init Module
        """
        self.future_look_ahead = [0, 5, 10, 15, 20]
        self.pose_feature = NonTalkingPoseFeature()
        self.feature_db = DefaultMotionFeatureDatabase(
            db,
            NonTalkingPoseFeature(),
            self.future_look_ahead,
            db_path=feature_path,
            db_file_name=feature_file_name,
        )
        self.idle_module = IdleModule(db, idle_file)
        self.transition_module = TransitionModule(db.get_frame_time())
        self.tag_processing_module = TagProcessingModule(
            db, phase_file, self.pose_feature, self.feature_db
        )
        self.pose_feature.update_look_ahead(self.future_look_ahead)
        history = NonTalkingHistoryFeature(look_behind=[0,5,10,15,20,25])

        """
        Init parameters
        """
        self.translation_offset = np.zeros(3)
        self.play_state_list = ["play", "transition", "loop"]
        self.motion_state_list = ["normal_tag", "duration_tag", "idle"]
        self.current_play_state = "play"
        self.current_motion_state = "idle"
        self.current_motion = self.idle_module.current_motion
        self.idx_current = 0
        self.len_motion = len(self.current_motion)
        self.past_pose = self.current_motion[0]
        self.idle_transition_duration = 60
        self.retract_transition_duration = 45

    """
    밖에서 호출되는 함수
    """

    def set_idle_transition_duration(self, duration: int):
        self.idle_transition_duration = duration

    def set_tag_input(
        self,
        pose: Frame,
        motion_history: deque,
        motion_future: deque,
        motion_tag: string = "Untagged",
        duration_tag: int = -1,
        blend_duration: int = 30,
    ):
        """
        motion_tag 와 duration tag를 받아서 다음 모션 정보를 생성
        motion_tag가 없는 경우 untagged
        duration_tag가 없는 경우 -1 을 넣는다.
        """
        self.tag_processing_module.reset()
        tagged_motion_info = self.tag_processing_module.search_tagged_motion(
            motion_future, motion_tag, blend_duration=blend_duration
        )
        processed_tag_info = self.tag_processing_module.process_matching_profile(
            *tagged_motion_info,
            blend_duration=blend_duration,
            duration_tag=duration_tag
        )
        self.transition_module.init_motion_transition(
            motion_history.pop(),
            pose,
            target_motion=processed_tag_info[0],
            idx_target_motion_cut=processed_tag_info[1],
            blend_dur=blend_duration,
            is_moving=processed_tag_info[2],
        )
        self.translation_offset = self.transition_module.root_blender.transl_offset
        self.current_motion = processed_tag_info[0]
        self.idx_current = processed_tag_info[1]
        self.current_play_state = "transition"
        if duration_tag == -1:
            self.current_motion_state = "normal_tag"
            self.len_motion = len(self.current_motion)
        else:
            self.current_motion_state = "duration_tag"

    def get_pseudo_future(self, idx_future):
        """
        Pseudo 미래를 반환하는 함수
        """
        if self.current_play_state == "loop":
            loop_start = self.tag_processing_module.idx_loop_start
            loop_cnt = (
                self.idx_current
                + idx_future
                - self.tag_processing_module.idx_retract_start
            )
            loop_len = self.tag_processing_module.loop_len
            return self.current_motion[loop_start + loop_cnt % loop_len]

        elif self.idx_current + idx_future < self.len_motion:
            return self.current_motion[self.idx_current + idx_future]
        else:
            return self.current_motion[self.len_motion - 1]

    def get_frame_chunk(self, cnt):
        frame_chunk = []
        for i in range(cnt):
            frame_chunk.append(self.get_next_frame())
        return frame_chunk

    def get_frame_angle_chunk(self, cnt, degree_order="ZXY"):
        angle_chunk = []
        for i in range(cnt):
            frame = self.get_next_frame()
            global_trans = frame.get_root_transform() * frame.get_local_transform(0)
            local = frame.get_local_transforms()
            angle = []
            for i, loci in enumerate(local):
                if i == 0:
                    degree = global_trans.rotation.as_euler(degree_order, degrees=True)
                else:
                    degree = loci.rotation.as_euler(degree_order, degrees=True)
                angle.extend(degree)
            angle_chunk.append(angle)
        return angle_chunk

    """
    내부용 함수
    """

    def get_next_frame(
        self,
    ):
        if self.current_play_state == "transition":
            frame, is_end_blending = self.transition_module.get_transition_frame(
                self.current_motion[self.idx_current].fast_copy()
            )
            self.idx_current = (
                self.idx_current + 1
                if self.transition_module.moving_blend_flag
                else self.idx_current
            )
            if is_end_blending:
                self.current_play_state = "play"
        elif self.current_play_state == "play":
            frame = shift_root(
                self.current_motion[self.idx_current].fast_copy(),
                self.translation_offset,
            )
            self.idx_current += 1
            if self.current_motion_state == "duration_tag":
                if self.idx_current >= self.tag_processing_module.hold_end:
                    self.tag_processing_module.reset()
                    self.switch_to_retract(frame)
                elif self.idx_current >= self.tag_processing_module.idx_retract_start:
                    self.init_loop_motion()
                    self.current_play_state = "loop"
            elif (
                self.current_motion_state == "normal_tag"
                or self.current_motion_state == "idle"
            ):
                if self.idx_current >= self.len_motion:
                    self.switch_to_idle(frame)
        elif self.current_play_state == "loop":
            frame = shift_root(self.get_loop_motion(), self.translation_offset)
            self.idx_current += 1
            if self.idx_current >= self.tag_processing_module.hold_end:
                self.tag_processing_module.reset()
                self.switch_to_retract(frame)
        else:
            raise Exception("Not a valid state :" + self.current_play_state)
        self.past_pose = frame
        return frame

    def switch_to_idle(self, current_frame):
        """
        모션이 끝난 경우 next motion으로 transition
        Transition할 motion clip의 idx는 next motion의 index 0 ~ len(motion) // 3 범위에서 찾음
        next idle motion 미리 생성
        """
        target_motion = self.idle_module.next_motion
        idx_next_motion = self.idle_module.idx_next_motion

        motion_future = deque()
        for idx_future in self.future_look_ahead:
            motion_future.append(self.get_pseudo_future(idx_future - 1))
        current_motion_feature = (
            self.pose_feature.compute_single_frame_feature_from_frame(motion_future)
        )
        target_motion_feature = self.feature_db._gesture_feature_DB[idx_next_motion][0][
            0
        ]
        self.len_motion = len(target_motion)
        idx_find_range = self.len_motion // 3 if self.idle_module.is_idle else self.idle_module.frm_hold

        idx_target_motion_cut, _ = find_single_cut_idx(
            current_motion_feature=current_motion_feature,
            target_motion_feature=target_motion_feature,
            idx_feat_end= idx_find_range
        )

        self.transition_module.init_motion_transition(
            front_first_frame=self.past_pose,
            front_second_frame=current_frame,
            target_motion=target_motion,
            idx_target_motion_cut=idx_target_motion_cut,
            blend_dur=self.idle_transition_duration,
            is_moving= False,
        )
        self.current_motion = target_motion
        self.translation_offset = self.transition_module.root_blender.transl_offset
        self.current_play_state = "transition"
        self.current_motion_state = "idle"
        self.idx_current = idx_target_motion_cut
        self.idle_module.generate_next_idle_motion()

    def switch_to_retract(self, current_frame):
        motion_future = deque()
        for idx_future in self.future_look_ahead:
            motion_future.append(self.get_pseudo_future(idx_future))

        searched_info = self.tag_processing_module.search_tagged_motion(
            motion_future,
            motion_tag="Untagged",
            start_feature="Retract",
            end_feature="End",
            blend_duration= self.retract_transition_duration
        )
        processed_tag_info = self.tag_processing_module.process_matching_profile(
            *searched_info,
            blend_duration=self.retract_transition_duration,
            duration_tag=-1
        )
        target_motion = processed_tag_info[0]
        idx_target_motion_cut = processed_tag_info[1]
        self.transition_module.init_motion_transition(
            front_first_frame=self.past_pose,
            front_second_frame=current_frame,
            target_motion=target_motion,
            idx_target_motion_cut=idx_target_motion_cut,
            blend_dur=self.retract_transition_duration,
            is_moving=True,
        )
        self.current_motion = target_motion
        self.translation_offset = self.transition_module.root_blender.transl_offset
        self.len_motion = len(self.current_motion)
        self.idx_current = idx_target_motion_cut
        self.current_play_state = "transition"
        self.current_motion_state = "normal_tag"

    def init_loop_motion(
        self,
    ):
        loop_start = self.tag_processing_module.idx_loop_start
        loop_end = self.tag_processing_module.idx_retract_start - 1
        if loop_end - loop_start < 15:
            self.tag_processing_module.loop_motion = [
                self.current_motion[loop_end] for j in range(15)
            ]
            return
        blend_dur = min(45, loop_end - loop_start + 25)
        self.transition_module.init_motion_transition(
            front_first_frame=self.current_motion[loop_end - 1],
            front_second_frame=self.current_motion[loop_end],
            target_motion=self.current_motion,
            idx_target_motion_cut=loop_start,
            blend_dur=blend_dur,
            is_moving=False,
            is_loop = True
        )

    def get_loop_motion(
        self,
    ):
        loop_cnt = self.idx_current - self.tag_processing_module.idx_retract_start
        if (
            loop_cnt < self.tag_processing_module.loop_len
            and self.tag_processing_module.loop_len >= 15
        ):
            """
            Put looping motion
            """
            idx_hold_loop = self.tag_processing_module.idx_loop_start + loop_cnt
            frame = self.transition_module.get_loop_frame(
                self.current_motion[idx_hold_loop].fast_copy()
            )
            self.tag_processing_module.loop_motion.append(frame)
        return self.tag_processing_module.loop_motion[
            loop_cnt % self.tag_processing_module.loop_len
        ].fast_copy()
