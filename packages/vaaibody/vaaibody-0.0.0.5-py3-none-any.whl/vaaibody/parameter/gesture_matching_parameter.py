import numpy as np

# USE_AUDIO = ["default", "slicing", "all"]
# USE_BEAT = ["all", "only_beat", "slicing"]
# SLICE_WITH_BEAT = ["slicing"]

TH_UPPER = [
    "b_r_forearm",
    "b_r_wrist",
    "b_r_index1",
    "b_r_pinky1",
    "b_l_forearm",
    "b_l_wrist",
    "b_l_index1",
    "b_l_pinky1",
]
TH_LOWER = ["b_r_upleg", "b_r_leg", "b_r_foot", "b_l_upleg", "b_l_leg", "b_l_foot"]
MCS_UPPER = [
    "RightForeArm",
    "RightHand",
    "RightFinger2Metacarpal",
    "RightFinger5Metacarpal",
    "LeftForeArm",
    "LeftHand",
    "LeftFinger2Metacarpal",
    "LeftFinger5Metacarpal",
]
MCS_UPPER_2 = [
    "Spine4",
    "RightArm",
    "RightShoulder",
    "RightForeArm",
    "RightHand",
    "RightFinger1Metacarpal",
    "RightFinger2Metacarpal",
    "RightFinger3Metacarpal",
    "RightFinger4Metacarpal",
    "RightFinger5Metacarpal",
    "LeftArm",
    "LeftShoulder",
    "LeftForeArm",
    "LeftHand",
    "LeftFinger1Metacarpal",
    "LeftFinger2Metacarpal",
    "LeftFinger3Metacarpal",
    "LeftFinger4Metacarpal",
    "LeftFinger5Metacarpal",
]
MCS_LOWER = [
    "LeftThigh",
    "LeftShin",
    "LeftFoot",
    "LeftToe",
    "RightThigh",
    "RightShin",
    "RightFoot",
    "RightToe",
]
MCS_LOWER_BLENDING = [
    "Hips",
    "LeftThigh",
    "LeftShin",
    "LeftFoot",
    "LeftToe",
    "RightThigh",
    "RightShin",
    "RightFoot",
    "RightToe",
]

MCS_SPINES = ["Spine1", "Spine2", "Spine3", "Spine4", "Neck", "Head"]


MCS_NON = [
    "Head_e",
    "Spine4",
    "RightForeArm",
    "RightHand",
    "RightFinger1Distal",
    "RightFinger5Distal",
    "RightToe_e",
    "LeftForeArm",
    "LeftHand",
    "LeftFinger1Distal",
    "LeftFinger5Distal",
    "LeftToe_e",
]
