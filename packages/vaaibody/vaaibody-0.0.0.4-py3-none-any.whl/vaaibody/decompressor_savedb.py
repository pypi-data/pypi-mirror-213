import struct
import sys

import matplotlib.pyplot as plt
import numpy as np
import torch
from scipy.spatial.transform import Rotation as R
from torch.utils.tensorboard import SummaryWriter

from core.database import MotionDatabase, MotionFeatureDatabase
from core.skeleton import Skeleton
from decompressor import Compressor, Decompressor
from decompressor_util import *
from utilities import quat, txform
from utilities.exporter import Exporter

# Load
bvh_name = "data/matching_data/rhythm_motion/VAAI_Short_01_02.bvh"
bvh_npz_path = "data/matching_data/rhythm_motion_npz/"
audio_db_path = "data/matching_data/rhythm_audio"
silent_db_path = "data/matching_data/silent_release"
# silent_db_path = "data/motion/Gesture_Before"

test_audio_path = "data/audio/Test/TTS_Hi.wav"

skeleton = Skeleton(name="KSW")
skeleton.load_hierarchy_from_bvh(bvh_name)

# sil
# motion_database = MotionDatabase(skeleton, silent_db_path, is_preload=True)
# feature_database = MotionFeatureDatabase(motion_database)
# test_n_frame = 71

# gesture
motion_database = MotionDatabase(skeleton, bvh_npz_path, use_npz=True)
feature_database = MotionFeatureDatabase(
    motion_database,
    db_path="data/matching_data",
    db_file_name="wv_feature_no_aug.pickle",
)
test_n_frame = 300

n_motion = motion_database.num_motion()
n_joint = 61
n_latent = 64
frame_size = 300

# Prepare X
X, _ = get_X(feature_database)
n_features = X.shape[1]

# Prepare Y
Ypos, Yrot, Yvel, Yang = get_Y(motion_database, n_motion, n_joint, frame_size)
n_frame = len(Ypos)

# parent list
parents = get_parents_list(motion_database)


# Parameters

seed = 1234
batch_size = 32
lr = 0.001
n_iter = 500000
window = 10  # todo
frame_time = 0.0166667  # dt

# Compute world space
print(Ypos.shape, Yrot.shape, Yvel.shape, Yang.shape)
print(parents)
Grot, Gpos, Gvel, Gang = quat.fk_vel(Yrot, Ypos, Yvel, Yang, parents)

# print(Grot.shape, Gpos.shape, Gvel.shape, Gang.shape)
# (53500, 23, 4) (53500, 23, 3) (53500, 23, 3) (53500, 23, 3)

# Compute character space

Qrot = quat.inv_mul(Grot[:, 0:1], Grot)
Qpos = quat.inv_mul_vec(Grot[:, 0:1], Gpos - Gpos[:, 0:1])
Qvel = quat.inv_mul_vec(Grot[:, 0:1], Gvel)
Qang = quat.inv_mul_vec(Grot[:, 0:1], Gang)
# print(Qrot.shape, Qpos.shape, Qvel.shape, Qang.shape)
# (53500, 23, 4) (53500, 23, 3) (53500, 23, 3) (53500, 23, 3)

# Compute transformation matrix
Yxfm = quat.to_xform(Yrot)
Qxfm = quat.to_xform(Qrot)
# print("Yxfm.shape, Qxfm.shape", Yxfm.shape, Qxfm.shape)
# Yxfm.shape, Qxfm.shape (53500, 23, 3, 3) (53500, 23, 3, 3)

# Compute two-column transformation matrix

Ytxy = quat.to_xform_xy(Yrot).astype(np.float32)
Qtxy = quat.to_xform_xy(Qrot).astype(np.float32)
# print("Ytxy.shape, Qtxy.shape", Ytxy.shape, Qtxy.shape)
# Ytxy.shape, Qtxy.shape (53500, 23, 3, 2) (53500, 23, 3, 2)

# Compute local root velocity

# Yrvel = quat.inv_mul_vec(Yrot[:, 0], Yvel[:, 0])
# Yrang = quat.inv_mul_vec(Yrot[:, 0], Yang[:, 0])
# print("Yrvel.shape, Yrang.shape", Yrvel.shape, Yrang.shape)
# Yrvel.shape, Yrang.shape (53500, 3) (53500, 3)

# Compute extra outputs (contacts)

# Compute means/stds

Ypos_scale = Ypos[:, 1:].std()
Ytxy_scale = Ytxy[:, 1:].std()
Yvel_scale = Yvel[:, 1:].std()
Yang_scale = Yang[:, 1:].std()

# print(Ypos.shape, Ypos[:,1:].shape, Ypos[:,1:].std().shape)
# (53500, 23, 3) (53500, 22, 3) ()

Qpos_scale = Qpos[:, 1:].std()
Qtxy_scale = Qtxy[:, 1:].std()
Qvel_scale = Qvel[:, 1:].std()
Qang_scale = Qang[:, 1:].std()

# Yrvel_scale = Yrvel.std()
# Yrang_scale = Yrang.std()

decompressor_mean_out, decompressor_std_out = get_decompressor_mean_std(
    Ypos, Ytxy, Yvel, Yang
)
compressor_mean_in, compressor_std_in = get_compressor_mean_std(
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
)

# Make PyTorch tensors

Ypos = torch.as_tensor(Ypos).to(torch.float32)
Yrot = torch.as_tensor(Yrot).to(torch.float32)
Ytxy = torch.as_tensor(Ytxy).to(torch.float32)
Yvel = torch.as_tensor(Yvel).to(torch.float32)
Yang = torch.as_tensor(Yang).to(torch.float32)

Qpos = torch.as_tensor(Qpos).to(torch.float32)
Qrot = torch.as_tensor(Qrot).to(torch.float32)
Qxfm = torch.as_tensor(Qxfm).to(torch.float32)
Qtxy = torch.as_tensor(Qtxy).to(torch.float32)
Qvel = torch.as_tensor(Qvel).to(torch.float32)
Qang = torch.as_tensor(Qang).to(torch.float32)

# Make networks

network_compressor = Compressor(len(compressor_mean_in), n_latent)

save_compressed_database(
    network_compressor,
    [Ypos, Ytxy, Yvel, Yang, Qpos, Qtxy, Qvel, Qang],
    n_frame,
    compressor_mean_in,
    compressor_std_in,
    feature_database,
)
