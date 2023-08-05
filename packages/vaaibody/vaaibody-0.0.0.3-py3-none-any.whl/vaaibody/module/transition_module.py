from core.blending import BlendingInertialization, RootBlender, RootInertialization
from core.frame import Frame
from core.motion import Motion


class TransitionModule(object):
    def __init__(self, frame_time: float) -> None:
        self.frame_time = frame_time
        self.blend_dur = 60
        self.reset_transition_info()

    def init_motion_transition(
        self,
        front_first_frame: Frame,
        front_second_frame: Frame,
        target_motion: Motion,
        idx_target_motion_cut: int,
        blend_dur: int,
        is_moving: bool = False,
        is_loop:bool = False
    ):
        """
        Motion Transition을 Inertialization을 이용하여 초기화함
        Args
            front_first_frame: 지금 모션의 직전 frame, root가 보정되어 있어야 한다.
            front_second_frame: 지금 모션의 지금 frame, root가 보정되어 있어야 한다.
            blend_dur: duration
            is_moving: moving inertialization인지 아닌지
        """
        back_target_frame = target_motion[idx_target_motion_cut]
        if is_moving:
            moving_target = back_target_frame
            vel_target = None
            acc_target = None
            vel_reducer = target_motion[idx_target_motion_cut + 1]
        else:
            moving_target = back_target_frame
            vel_target = target_motion[idx_target_motion_cut + 1]
            acc_target = target_motion[idx_target_motion_cut + 2]
            vel_reducer = None

        self.blender = BlendingInertialization(
            front_second_frame,
            front_first_frame,
            back_target_frame,
            blend_dur,
            self.frame_time,
            is_frame=True,
            moving_target=moving_target,
            target_vel=vel_target,
            target_acc=acc_target,
            vel_reducer=vel_reducer,
        )
        if is_loop:
            self.root_blender = RootBlender(
                front_second_frame,
                target_motion[idx_target_motion_cut],
                blend_dur,
                is_moving
            )
        else:
            self.root_blender = RootInertialization(
                front_second_frame,
                front_first_frame,
                back_target_frame,
                blend_dur,
                is_moving,
                self.frame_time
            )
        self.moving_blend_flag = is_moving
        self.blend_dur = blend_dur
        self.blending_cnt = 0

    def reset_transition_info(
        self,
    ):
        """
        Transition 정보를 초기화한다.
        Args
            blender: 현재 blender (Blender)
            moving_blend_flag: moving inertialization인지 여부 (bool)
            blending_cnt: 블렌딩 되는 카운트
        """
        self.blender = None
        self.moving_blend_flag = False
        self.blending_cnt = 0

    def get_transition_frame(self, current_pose):
        self.blender.apply_frame_blending(current_pose, self.blending_cnt)
        self.root_blender.root_blending(current_pose,self.blending_cnt)
        self.blending_cnt += 1

        return current_pose, self.blending_cnt >= self.blend_dur

    def get_loop_frame(self, current_pose):
        self.blender.apply_frame_blending(current_pose, self.blending_cnt)
        self.root_blender.root_loop_blending(current_pose, self.blending_cnt)
        self.blending_cnt += 1

        return current_pose
