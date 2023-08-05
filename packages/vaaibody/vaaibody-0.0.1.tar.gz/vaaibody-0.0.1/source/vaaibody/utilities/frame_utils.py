import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt, savgol_filter
from scipy.spatial.transform import Rotation as R
from vaaibody.core.skeleton import Transform
from vaaibody.core.motion import Motion

# def spin_180(rotation:R):
#     mirror_rot = np.array([[-1,-1,1],[1,1,-1],[1,1,-1]])
#     return mirror_rot * rotation.as_matrix()


def shift_root(frame, translation_offset):
    root_ori = frame.get_root_transform().rotation
    transl = frame.get_root_transform().translation + translation_offset
    new_root = Transform(root_ori, transl)
    frame.set_root_transform(new_root)
    return frame


def find_single_cut_idx(
    current_motion_feature: np.ndarray,
    target_motion_feature: np.ndarray,
    idx_feat_start: int = 0,
    idx_feat_end: int = -1,
):
    """
    Args
        current_motion_feature:
        target_motion_feature:
        idx_feat_start: feature를 찾기 시작할 frame index
        idx_feat_end: feature를 찾기 끝낼 frame index
    """
    if idx_feat_end == -1:
        idx_feat_end = target_motion_feature.shape[0]
    if idx_feat_start >= idx_feat_end:
        return idx_feat_start, 100000000
    feature_of_interest = target_motion_feature[idx_feat_start:idx_feat_end]
    costs = np.sqrt((current_motion_feature - feature_of_interest) ** 2).mean(axis=-1)
    idx_result = np.argmin(costs)
    return idx_result + idx_feat_start, costs[idx_result]


def find_multi_cut_idx(
    current_motion_feature: np.ndarray,
    target_motion_feature: np.ndarray,
):
    """
    Args
        current_motion_feature:
        target_motion_feature:
    """
    costs = np.sqrt((current_motion_feature - target_motion_feature) ** 2).mean(axis=-1)
    idx_result = np.argmin(costs)
    return idx_result, costs[idx_result]


def single_cont_conversion(diff, current_np_frame):
    current_np_frame = np.where(diff > 180, current_np_frame + 360, current_np_frame)
    current_np_frame = np.where(diff < -180, current_np_frame - 360, current_np_frame)
    return current_np_frame


def make_cont_frame(prev_np_frame, current_np_frame):
    diff = prev_np_frame - current_np_frame
    while np.any(diff > 180) or np.any(diff < -180):
        current_np_frame = single_cont_conversion(diff, current_np_frame)
        diff = prev_np_frame - current_np_frame
    return current_np_frame


def make_cont_frames(frames):
    # Frames : (# frames, 3 * (#joint + 1))
    num_frame = frames.shape[0]
    for i in range(1, num_frame):
        frames[i] = make_cont_frame(frames[i - 1], frames[i])
    return frames


def single_range_conversion(current_np_frame):
    current_np_frame = np.where(
        current_np_frame > 180, current_np_frame - 360, current_np_frame
    )
    current_np_frame = np.where(
        current_np_frame < -180, current_np_frame + 360, current_np_frame
    )
    return current_np_frame


def make_range_frame(current_np_frame):
    while np.any(current_np_frame > 180) or np.any(current_np_frame < -180):
        current_np_frame = single_range_conversion(current_np_frame)
    return current_np_frame


def convert_frames_range(frames):
    # Frames : (# frames, 3 * (#joint + 1))
    num_frame = frames.shape[0]
    for i in range(num_frame):
        make_range_frame(frames[i])
    return frames


def filter_frames(frames, filter_name: str, args={}):
    """
    Note that angle conversion is needed since the angle is expressed in range (-180, 180)
    For example, when x-angle of the spine is expressed as 178, 179, -178,
    the angle difference is actually 1, 3 but it is calculated as 1, 357.
    Therefore, we need to convert the angle to 178, 179, 182 ... and so on as calculation
    and then convert those angle to (-180, 180) after filtering
    """
    print("Now filtering process")
    start_time = time.time()
    filter = None
    np_frames = []
    for frame in frames:
        raw_frame = frame.get_raw_frame()
        np_frames.append(raw_frame)
    np_frames = make_cont_frames(np.array(np_frames))

    if filter_name == "sg":
        filter = savgol_filter
        w_l = 6
        p_o = 3
        if args.get("window_length") is not None:
            w_l = args["window_length"]
        if args.get("poly_order") is not None:
            p_o = args["poly_order"]

        filtered_frames = convert_frames_range(filter(np_frames, w_l, p_o, axis=0))

        for i in range(filtered_frames.shape[0]):
            frames[i].set_by_raw_rotations(filtered_frames[i])

    elif filter_name == "lowpass" or filter_name == "lpf":
        filter = filtfilt
        low_order = 4
        Wn = 0.1
        if args.get("low_order") is not None:
            low_order = args["low_order"]
        if args.get("Wn") is not None:
            Wn = args["Wn"]
        b, a = butter(N=low_order, Wn=Wn, btype="low")
        filtered_frames = convert_frames_range(
            filter(b, a, np_frames, axis=0, padlen=50)
        )

        for i in range(filtered_frames.shape[0]):
            # print(i, " th")
            # print("ori", np_frames[i, 30:33])
            # print("filtered", filtered_frames[i, 30:33])
            frames[i].set_by_raw_rotations(filtered_frames[i])

    else:
        print("Invalid filter, return non-filtered result")

    print("Filtering takes {}seconds".format(time.time() - start_time))
    return frames


def get_angular_vel(motion):
    """
    Return angular velocity with deg/sec
    """
    ang_vel = []
    frm_time = motion.frame_time
    for i in range(len(motion)):
        if i == 0:
            ang_vel.append(
                (
                    np.array(motion[i + 1].get_raw_frame())
                    - np.array(motion[i].get_raw_frame())
                )[3:]
                / frm_time
            )
        elif i == len(motion) - 1:
            ang_vel.append(
                (
                    np.array(motion[i].get_raw_frame())
                    - np.array(motion[i - 1].get_raw_frame())
                )[3:]
                / frm_time
            )
        else:
            ang_vel.append(
                (
                    np.array(motion[i + 1].get_raw_frame())
                    - np.array(motion[i - 1].get_raw_frame())
                )[3:]
                / (2 * frm_time)
            )
    return np.array(ang_vel)


def get_position_vel(motion):
    skel = motion.skeleton
    n_joint = skel.num_joints()
    pose_vel = []
    frm_time = motion.frame_time
    # float_formatter = "{:.2f}".format
    # np.set_printoptions(formatter={'float_kind':float_formatter})
    for i in range(len(motion)):
        prev = motion[max(0, i - 1)]
        after = motion[min(len(motion) - 1, i + 1)]
        i_vel = np.zeros(n_joint * 3)
        for joint_idx in range(n_joint):
            if joint_idx == 0:
                dev = (
                    after.get_global_transform(joint_idx).translation
                    - prev.get_global_transform(joint_idx).translation
                )
            else:
                dev = (
                    after.get_component_transform(joint_idx).translation
                    - prev.get_component_transform(joint_idx).translation
                )
            if i == 0 or i == len(motion) - 1:
                vel = dev / frm_time
            else:
                vel = dev / (2 * frm_time)
            i_vel[3 * joint_idx : 3 * (joint_idx + 1)] = vel
        pose_vel.append(i_vel)
    return np.array(pose_vel, dtype="f")


def plot_position_vel(motion):
    plt.close("all")
    vel = get_position_vel(motion).transpose()
    j_dict = motion.skeleton.joint_dict
    dt = motion.frame_time
    t = np.arange(0, motion.num_frame())
    # t = np.arange(0, motion.num_frame()) * dt
    fig, axs = plt.subplots(3, 1, figsize=(10, 6))
    for i in range(vel.shape[0]):
        if i % 3 == 0:
            if j_dict["LeftHand"] == i // 3 or j_dict["RightHand"] == i // 3:
                axs[0].plot(t, vel[i])
    axs[0].set_ylabel("x-axis vel")
    for i in range(vel.shape[0]):
        if i % 3 == 1:
            if j_dict["LeftHand"] == i // 3 or j_dict["RightHand"] == i // 3:
                axs[1].plot(t, vel[i])
    axs[1].set_ylabel("y-axis vel")
    for i in range(vel.shape[0]):
        if i % 3 == 2:
            if j_dict["LeftHand"] == i // 3 or j_dict["RightHand"] == i // 3:
                axs[2].plot(t, vel[i])
    axs[2].set_xlabel("Time")
    axs[2].set_ylabel("z-axis vel")
    fig.tight_layout()
    plt.draw()
    plt.pause(0.001)


def visualize_gaze_distribution(motion):
    # plt.close("all")
    head_idx = motion.skeleton.joint_dict["Head"]
    j = motion.skeleton.joints[head_idx]
    x = np.zeros(len(motion))
    y = np.zeros(len(motion))
    z = np.zeros(len(motion))
    u = np.zeros(len(motion))
    v = np.zeros(len(motion))
    w = np.zeros(len(motion))

    for i in range(len(motion)):
        current_frame = motion[i]
        # end_trans = np.matmul(current_frame.get_global_transform(head_idx).rotation_np, j._end_site_transform.translation)
        # head = current_frame.get_global_transform(head_idx).translation + end_trans /2
        front = np.matmul(
            current_frame.get_global_transform(head_idx).rotation_np,
            np.array([0, 0, 1]),
        )
        u[i] = front[0]
        v[i] = -front[2]
        w[i] = front[1]

    ax = plt.figure("Gaze", figsize=(10, 10)).add_subplot(projection="3d")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Z axis")
    ax.set_zlabel("Y axis")
    ax.set_zticklabels([])
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.quiver(x, y, z, u, v, w, arrow_length_ratio=0.1, alpha=0.01)

    fig = plt.figure("Frontal view", figsize=(6, 6))
    ax1 = plt.figure("Frontal view").add_subplot(1, 1, 1)
    # ax2 = plt.figure("2D").add_subplot(1, 2, 2)
    ax1.set_xlim(-1, 1)
    ax1.set_ylim(-1, 1)
    # ax2.set_xlim(-1, 1)
    # ax2.set_ylim(-1, 1)
    ax1.set_title("Frontal view")
    # ax2.set_title("Side view")

    ax1.scatter(u, w, alpha=0.1)
    # ax2.scatter(v+1,w, alpha= 0.1)

    plt.draw()
    plt.pause(0.001)


def add_gaze_distribution(motion):
    head_idx = motion.skeleton.joint_dict["Head"]
    j = motion.skeleton.joints[head_idx]
    x = np.zeros(len(motion))
    y = np.zeros(len(motion))
    z = np.zeros(len(motion))
    u = np.zeros(len(motion))
    v = np.zeros(len(motion))
    w = np.zeros(len(motion))

    for i in range(len(motion)):
        current_frame = motion[i]
        # end_trans = np.matmul(current_frame.get_global_transform(head_idx).rotation_np, j._end_site_transform.translation)
        # head = current_frame.get_global_transform(head_idx).translation + end_trans /2
        front = np.matmul(
            current_frame.get_global_transform(head_idx).rotation_np,
            np.array([0, 0, 1]),
        )
        u[i] = front[0]
        v[i] = -front[2]
        w[i] = front[1]

    ax = plt.figure("Gaze").get_axes()[0]
    ax.quiver(x, y, z, u, v, w, arrow_length_ratio=0.1, alpha=0.01)

    ax1 = plt.figure("Frontal view").get_axes()[0]

    ax1.scatter(u, w, alpha=0.1)
    plt.draw()
    # plt.pause(100)
    plt.pause(0.001)


def tick_graph():
    plt.draw()
    plt.pause(0.001)
