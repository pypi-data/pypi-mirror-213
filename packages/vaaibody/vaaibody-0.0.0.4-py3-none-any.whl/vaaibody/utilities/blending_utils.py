from core.blending import *
from core.frame import Frame
from core.motion import Motion


def brute_add(motion1: Motion, motion2: Motion, path=None):
    brute_motion = motion1.copy()
    if path is not None:
        brute_motion._file_path = path
    brute_motion.append(motion2.copy())
    return brute_motion


def motion_straight_insertion_blend(
    motion1: Motion, motion2: Motion, blend_dur=60, path="Straight_blend"
):
    frame_time = motion1.frame_time
    len_motion = len(motion1)
    first_motion = motion1[-2].copy()
    second_motion = motion1[-1].copy()
    current_root = second_motion.get_root_transform()
    target_frame = motion2[0].copy()
    new_root = target_frame.get_root_transform()
    root_offset = current_root * new_root.inverse()
    target_frame.set_root_transform(root_offset * target_frame.get_root_transform())
    blender = BlendingInertialization(
        second_motion, first_motion, target_frame, blend_dur, frame_time, is_frame=True
    )
    root_blender = RootBlender(second_motion, motion2[blend_dur].copy(), blend_dur)

    frames = []
    for i in range(len_motion):
        frames.append(motion1[i].copy())

    for blend_cnt in range(0, blend_dur):
        current_pose = motion2[0].copy()
        current_pose = blender.apply_frame_blending(current_pose, blend_cnt)
        current_pose = root_blender.root_blending(current_pose, blend_cnt)
        frames.append(current_pose)

    for i in range(0, len(motion2)):
        frames.append(motion2[i].copy())

    idle_blended_motion = Motion(motion1.skeleton, frames, frame_time, file_path=path)
    return idle_blended_motion


def motion_straight_blend(
    motion1: Motion, motion2: Motion, blend_dur=60, path="Straight_blend"
):
    frame_time = motion1.frame_time
    len_motion = len(motion1)
    first_motion = motion1[-2].copy()
    second_motion = motion1[-1].copy()
    current_root = second_motion.get_root_transform()
    target_frame = motion2[0].copy()
    new_root = target_frame.get_root_transform()
    root_offset = current_root * new_root.inverse()
    target_frame.set_root_transform(root_offset * target_frame.get_root_transform())
    blender = BlendingInertialization(
        second_motion, first_motion, target_frame, blend_dur, frame_time, is_frame=True
    )
    root_blender = RootBlender(second_motion, motion2[blend_dur].copy(), blend_dur)

    frames = []
    for i in range(len_motion):
        frames.append(motion1[i].copy())

    for blend_cnt in range(0, blend_dur):
        current_pose = motion2[blend_cnt].copy()
        current_pose = blender.apply_frame_blending(current_pose, blend_cnt)
        current_pose = root_blender.root_blending(current_pose, blend_cnt)
        frames.append(current_pose)

    for i in range(blend_dur, len(motion2)):
        frames.append(motion2[i].copy())

    idle_blended_motion = Motion(motion1.skeleton, frames, frame_time, file_path=path)
    return idle_blended_motion


def motion_random_blend(
    motion1: Motion, motion2: Motion, blend_dur=60, path="Straight_blend"
):
    frame_time = motion1.frame_time
    len_motion = len(motion1)
    first_motion = motion1[-2].copy()
    second_motion = motion1[-1].copy()
    current_root = second_motion.get_root_transform()
    target_frame = motion2[0].copy()
    new_root = target_frame.get_root_transform()
    root_offset = current_root * new_root.inverse()
    target_frame.set_root_transform(root_offset * target_frame.get_root_transform())
    blender = BlendingInertialization(
        second_motion, first_motion, target_frame, blend_dur, frame_time, is_frame=True
    )
    root_blender = RootBlender(second_motion, motion2[blend_dur].copy(), blend_dur)

    frames = []
    for i in range(len_motion):
        frames.append(motion1[i].copy())

    for blend_cnt in range(0, blend_dur):
        current_pose = motion2[blend_cnt].copy()
        current_pose = blender.apply_frame_blending(current_pose, blend_cnt)
        current_pose = root_blender.root_blending(current_pose, blend_cnt)
        frames.append(current_pose)

    for i in range(blend_dur, len(motion2)):
        frames.append(motion2[i].copy())

    idle_blended_motion = Motion(motion1.skeleton, frames, frame_time, file_path=path)
    return idle_blended_motion


def root_fixed_idle_list_blender(idle_frame: Frame, motion: Motion, blend_dur=None):
    frame_time = motion.frame_time
    len_motion = len(motion)
    if blend_dur is None:
        blend_duration = (len_motion - 1) // 2
    elif len_motion < blend_dur:
        blend_duration = (len_motion - 1) // 2
    else:
        blend_duration = blend_dur

    st_cnt = len_motion - blend_duration
    first_motion = motion[st_cnt - 2].copy()
    second_motion = motion[st_cnt - 1].copy()

    current_root = second_motion.get_root_transform()
    new_root = idle_frame.get_root_transform()
    root_offset = current_root * new_root.inverse()
    root_recon = root_offset * new_root
    new_root.translation = root_recon.translation
    target_frame = idle_frame.copy()
    target_frame.set_root_transform(root_offset)
    blender = BlendingInertialization(
        second_motion,
        first_motion,
        target_frame,
        blend_duration,
        frame_time,
        is_frame=True,
    )

    frames = []
    for i in range(st_cnt):
        frames.append(motion[i].copy())

    for blend_cnt in range(1, blend_duration + 1):
        current_pose = idle_frame.copy()
        # current_pose.set_root_transform(root_offset * idle_frame.get_root_transform())
        current_pose = blender.apply_frame_blending(current_pose, blend_cnt)
        # current_pose.set_root_transform(root_offset * current_pose.get_root_transform())
        frames.append(current_pose)

    idle_blended_motion = Motion(
        motion.skeleton, frames, frame_time, file_path="Gen_idle.bvh"
    )
    return idle_blended_motion


def root_fixed_idle_blender2(
    idle_frame: Frame, motion: Motion, blend_dur=None, path="default.bvh"
):
    frame_time = motion.frame_time
    len_motion = len(motion)
    if blend_dur is None:
        blend_duration = (len_motion - 1) // 2
    elif len_motion < blend_dur:
        blend_duration = (len_motion - 1) // 2
    else:
        blend_duration = blend_dur

    st_cnt = len_motion - blend_duration
    zero_motion = motion[0].copy()
    first_motion = motion[st_cnt - 2].copy()
    second_motion = motion[st_cnt - 1].copy()
    current_root = second_motion.get_root_transform()
    new_root = idle_frame.get_root_transform()
    root_offset = current_root * new_root.inverse()
    root_recon = root_offset * new_root
    target_frame = idle_frame.copy()
    target_frame.set_root_transform(root_recon)
    blender = BlendingInertialization(
        second_motion,
        first_motion,
        target_frame,
        blend_duration,
        frame_time,
        is_frame=True,
    )
    root_blender = RootInertialization(
        second_motion,
        first_motion,
        idle_frame.copy(),
        blend_duration,
        frame_time,
        is_frame=True,
    )
    # root_blender = RootBlender(zero_motion, idle_frame.copy(), len_motion)

    frames = []
    cnt = 0
    for i in range(st_cnt):
        # current_pose = root_blender.linear_root_blending(motion[i].copy(), cnt)
        # current_pose = root_blender.root_blending(motion[i].copy(), cnt)
        # frames.append(current_pose)
        frames.append(motion[i].copy())
        cnt += 1

    for blend_cnt in range(1, blend_duration + 1):
        current_pose = idle_frame.copy()
        current_pose.set_root_transform(root_offset * idle_frame.get_root_transform())
        current_pose = blender.apply_frame_blending(current_pose, blend_cnt)
        current_pose = root_blender.apply_frame_blending(current_pose, blend_cnt)
        # current_pose = root_blender.root_blending(current_pose, cnt)
        frames.append(current_pose)
        cnt += 1

    idle_blended_motion = Motion(motion.skeleton, frames, frame_time, file_path=path)
    return idle_blended_motion


def root_fixed_idle_blender(
    idle_frame: Frame, motion: Motion, blend_dur=None, path="default.bvh"
):
    frame_time = motion.frame_time
    len_motion = len(motion)
    if blend_dur is None:
        blend_duration = (len_motion - 1) // 2
    elif len_motion < blend_dur:
        blend_duration = (len_motion - 1) // 2
    else:
        blend_duration = blend_dur

    st_cnt = len_motion - blend_duration
    first_motion = motion[st_cnt - 2].copy()
    second_motion = motion[st_cnt - 1].copy()
    current_root = second_motion.get_root_transform()
    new_root = idle_frame.get_root_transform()
    root_offset = current_root * new_root.inverse()
    root_recon = root_offset * new_root
    target_frame = idle_frame.copy()
    target_frame.set_root_transform(root_recon)
    blender = BlendingInertialization(
        second_motion,
        first_motion,
        target_frame,
        blend_duration,
        frame_time,
        is_frame=True,
    )
    root_blender = RootBlender(second_motion, idle_frame.copy(), blend_duration)

    frames = []
    for i in range(st_cnt):
        frames.append(motion[i].copy())

    for blend_cnt in range(1, blend_duration + 1):
        current_pose = idle_frame.copy()
        current_pose.set_root_transform(root_offset * idle_frame.get_root_transform())
        current_pose = blender.apply_frame_blending(current_pose, blend_cnt)
        current_pose = root_blender.root_blending(current_pose, blend_cnt)
        frames.append(current_pose)

    idle_blended_motion = Motion(motion.skeleton, frames, frame_time, file_path=path)
    return idle_blended_motion


def root_fixed_idle_adder(
    idle_frame: Frame, motion: Motion, blend_duration=60, path="Idle_gen"
):
    frame_time = motion.frame_time
    len_motion = len(motion)

    first_motion = motion[len_motion - 2].copy()
    second_motion = motion[len_motion - 1].copy()
    current_root = second_motion.get_root_transform()
    new_root = idle_frame.get_root_transform()
    root_offset = current_root * new_root.inverse()
    # idle_frame.set_root_transform(root_offset * idle_frame.get_root_transform())
    blender = BlendingInertialization(
        second_motion,
        first_motion,
        idle_frame,
        blend_duration,
        frame_time,
        is_frame=True,
    )
    root_blender = RootBlender(second_motion, idle_frame.copy(), blend_duration)

    current_pose = second_motion

    frames = []
    for i in range(len_motion):
        frames.append(motion[i].copy())

    for blend_cnt in range(0, blend_duration):
        current_pose = idle_frame.copy()
        current_pose = blender.apply_frame_blending(current_pose, blend_cnt)
        current_pose = root_blender.root_blending(current_pose.copy(), blend_cnt)
        frames.append(current_pose)

    idle_blended_motion = Motion(motion.skeleton, frames, frame_time, file_path=path)
    return idle_blended_motion


def idle_insertion(idle_frame: Frame, motion: Motion, motion_cnt, idle_cnt, blend_dur):
    frame_time = motion.frame_time
    len_motion = len(motion)
    cnt = 0
    idx = 0
    motion_flag = True
    blend_flag = False
    idle_flag = False
    frames = []
    root_offset = None
    while idx < len_motion:
        if not blend_flag and motion_flag:
            if root_offset is None:
                frames.append(motion[idx].copy())
            else:
                new_motion = motion[idx].copy()
                new_motion.set_root_transform(
                    root_offset * new_motion.get_root_transform()
                )
                frames.append(new_motion)
            idx += 1
            cnt += 1
            if cnt == motion_cnt:
                cnt = 0
                blend_flag = True
        elif blend_flag and motion_flag:
            first_motion = motion[idx - 2].copy()
            second_motion = motion[idx - 1].copy()
            current_root = second_motion.get_root_transform()
            new_root = idle_frame.get_root_transform()
            if root_offset is None:
                root_offset = current_root * new_root.inverse()
            else:
                root_offset = root_offset * current_root * new_root.inverse()
            idle_frame.set_root_transform(root_offset * idle_frame.get_root_transform())
            blender = BlendingInertialization(
                second_motion,
                first_motion,
                idle_frame,
                blend_dur,
                frame_time,
                is_frame=True,
            )
            current_pose = second_motion
            for blend_cnt in range(0, blend_dur):
                current_pose = idle_frame.copy()
                current_pose = blender.apply_frame_blending(current_pose, blend_cnt)
                frames.append(current_pose)
                idx += 1
                if idx == len_motion:
                    break
            del blender
            motion_flag = False
            blend_flag = False
            idle_flag = True
        elif blend_flag and idle_flag:
            first_motion = idle_frame.copy()
            second_motion = idle_frame.copy()
            current_root = second_motion.get_root_transform()
            new_frame = motion[idx].copy()
            new_root = new_frame.get_root_transform()
            root_offset = current_root * new_root.inverse()
            new_frame.set_root_transform(root_offset * new_frame.get_root_transform())
            blender = BlendingInertialization(
                second_motion,
                first_motion,
                new_frame,
                blend_dur,
                frame_time,
                is_frame=True,
            )
            current_pose = second_motion
            for blend_cnt in range(0, blend_dur):
                current_pose = motion[idx].copy()
                current_pose = blender.apply_frame_blending(current_pose, blend_cnt)
                current_pose.set_root_transform(
                    root_offset * current_pose.get_root_transform()
                )
                frames.append(current_pose)
                idx += 1
                if idx == len_motion:
                    break
            del blender
            motion_flag = True
            blend_flag = False
            idle_flag = False
        elif not blend_flag and idle_flag:
            frames.append(idle_frame.copy())
            idx += 1
            cnt += 1
            if cnt == idle_cnt:
                cnt = 0
                blend_flag = True

    idle_blended_motion = Motion(
        motion.skeleton,
        frames,
        frame_time,
        file_path=motion.file_path[:-4] + "_inserted.bvh",
    )
    return idle_blended_motion
