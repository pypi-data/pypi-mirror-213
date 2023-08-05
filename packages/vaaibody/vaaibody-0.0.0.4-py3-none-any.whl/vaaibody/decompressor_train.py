import argparse
import sys

import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter

from core.database import MotionDatabase, MotionFeatureDatabase
from core.frame import Frame
from core.motion import Motion
from core.skeleton import Skeleton
from decompressor import Compressor, Decompressor
from decompressor_util import *
from utilities import quat, txform
from utilities.exporter import Exporter


def main(args):
    # Path
    bvh_name = args.bvh_name
    bvh_npz_path = args.bvh_npz_path
    audio_db_path = args.audio_db_path
    silent_db_path = args.silent_db_path
    test_audio_path = args.test_audio_path

    # train paramter
    seed = args.seed
    torch.manual_seed(args.seed)
    batch_size = args.batch_size
    lr = args.lr
    n_iter = args.n_iter
    window = args.window
    frame_time = args.frame_time

    skeleton = Skeleton(name="KSW")
    skeleton.load_hierarchy_from_bvh(bvh_name)

    motion_type = args.motion_type
    if motion_type == "gesture":
        # gesture
        motion_database = MotionDatabase(skeleton, bvh_npz_path, use_npz=True)
        feature_database = MotionFeatureDatabase(
            motion_database,
            db_path="data/matching_data",
            db_file_name="wv_feature_no_aug.pickle",
        )
        test_n_frame = 300
    elif motion_type == "silent":
        # sil
        motion_database = MotionDatabase(skeleton, silent_db_path, is_preload=True)
        feature_database = MotionFeatureDatabase(
            motion_database, db_path="data/matching_data"
        )
        test_n_frame = 71
    else:
        print("motion type error")
        exit()

    n_motion = motion_database.num_motion()
    n_joint = args.n_joint  # 61
    n_latent = args.n_latent  # 64
    frame_size = args.frame_size  # 300

    # Prepare X
    X, clip_idx_list = get_X(feature_database)
    n_features = X.shape[1]

    # Prepare Y
    Ypos, Yrot, Yvel, Yang = get_Y(motion_database, n_motion, n_joint, frame_size)
    print(Ypos.shape, Yrot.shape, Yvel.shape, Yang.shape)
    n_frame = len(Ypos)

    # parent list
    parents = get_parents_list(motion_database)
    print(parents)

    # Compute world space
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

    # Yrvel = torch.as_tensor(Yrvel).to(torch.float32)
    # Yrang = torch.as_tensor(Yrang).to(torch.float32)

    X = torch.as_tensor(X).to(torch.float32)

    # Make networks

    network_compressor = Compressor(len(compressor_mean_in), n_latent)
    # network_compressor.load_state_dict(torch.load("compressor.pt"))

    # network_compressor.load_state_dict(torch.load("gesture_velocityloss/compressor.pt"))
    network_decompressor = Decompressor(
        n_features + n_latent, len(decompressor_mean_out)
    )
    # network_decompressor.load_state_dict(torch.load("decompressor.pt"))

    # Function to generate test animation for comparison

    def generate_animation(idx_iter: int):
        with torch.no_grad():
            # Get slice of database for first clip

            n_samples = args.n_sample

            for idx_sample in range(n_samples):
                start = clip_idx_list[idx_sample][0]
                stop = clip_idx_list[idx_sample][1]

                # start = range_starts[2]
                # stop = min(start + 1000, range_stops[2])
                # start = 0
                # stop = 300

                Ygnd_pos = Ypos[start:stop][np.newaxis]
                Ygnd_rot = Yrot[start:stop][np.newaxis]
                Ygnd_txy = Ytxy[start:stop][np.newaxis]
                Ygnd_vel = Yvel[start:stop][np.newaxis]
                Ygnd_ang = Yang[start:stop][np.newaxis]

                Qgnd_pos = Qpos[start:stop][np.newaxis]
                Qgnd_txy = Qtxy[start:stop][np.newaxis]
                Qgnd_vel = Qvel[start:stop][np.newaxis]
                Qgnd_ang = Qang[start:stop][np.newaxis]

                # Ygnd_rvel = Yrvel[start:stop][np.newaxis]
                # Ygnd_rang = Yrang[start:stop][np.newaxis]

                Xgnd = X[start:stop][np.newaxis]

                # Pass through compressor

                Zgnd = network_compressor(
                    (
                        torch.cat(
                            [
                                Ygnd_pos[:, :, 1:].reshape([1, stop - start, -1]),
                                Ygnd_txy[:, :, 1:].reshape([1, stop - start, -1]),
                                Ygnd_vel[:, :, 1:].reshape([1, stop - start, -1]),
                                Ygnd_ang[:, :, 1:].reshape([1, stop - start, -1]),
                                Qgnd_pos[:, :, 1:].reshape([1, stop - start, -1]),
                                Qgnd_txy[:, :, 1:].reshape([1, stop - start, -1]),
                                Qgnd_vel[:, :, 1:].reshape([1, stop - start, -1]),
                                Qgnd_ang[:, :, 1:].reshape([1, stop - start, -1]),
                                # Ygnd_rvel.reshape([1, stop - start, -1]),
                                # Ygnd_rang.reshape([1, stop - start, -1]),
                            ],
                            dim=-1,
                        )
                        - compressor_mean_in
                    )
                    / compressor_std_in
                )

                # Pass through decompressor

                Ytil = (
                    network_decompressor(torch.cat([Xgnd, Zgnd], dim=-1))
                    * decompressor_std_out
                    + decompressor_mean_out
                )

                # Extract required components

                Ytil_pos = Ytil[:, :, 0 * (n_joint - 1) : 3 * (n_joint - 1)].reshape(
                    [1, stop - start, n_joint - 1, 3]
                )
                Ytil_txy = Ytil[:, :, 3 * (n_joint - 1) : 9 * (n_joint - 1)].reshape(
                    [1, stop - start, n_joint - 1, 3, 2]
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

                Ytil_rot = np.concatenate(
                    [Ygnd_rot[0][:, 0, :][:, np.newaxis], Ytil_rot], axis=1
                )
                Ytil_pos = np.concatenate(
                    [Ygnd_pos[0][:, 0, :][:, np.newaxis], Ytil_pos], axis=1
                )

                frames_gnd = []
                local_transforms_gnd = get_local_transform_from_posrot(
                    Ygnd_pos[0][:test_n_frame].cpu().numpy(),
                    Ygnd_rot[0][:test_n_frame].cpu().numpy(),
                )
                # for idx_frame in range(71):
                for idx_frame in range(test_n_frame):
                    frames_gnd.append(
                        Frame(
                            skeleton,
                            motion_database.get_motion(idx_sample)[
                                idx_frame
                            ].get_root_transform(),
                            # local_transforms_gnd[0][0],
                            local_transforms_gnd[idx_frame],
                        )
                    )
                searched_motion_gnd = Motion(skeleton, frames_gnd, frame_time)

                frames_til = []
                local_transforms_til = get_local_transform_from_posrot(
                    Ytil_pos[:test_n_frame], Ytil_rot[:test_n_frame]
                )
                for idx_frame in range(test_n_frame):
                    cur_frame = Frame(
                        skeleton,
                        motion_database.get_motion(idx_sample)[
                            idx_frame
                        ].get_root_transform(),
                        local_transforms_til[idx_frame],
                    )
                    cur_frame.set_root_transform(
                        frames_gnd[idx_frame].get_root_transform()
                    )
                    frames_til.append(cur_frame)

                searched_motion_til = Motion(skeleton, frames_til, frame_time)

                try:
                    if idx_iter < 10:
                        exporter_gnd = Exporter(
                            bvh_name,
                            "decompressor_Ygnd_"
                            + str(idx_iter)
                            + str(idx_sample)
                            + ".bvh",
                        )
                        exporter_gnd.init_export(len(searched_motion_gnd))
                        exporter_gnd.export_motion(searched_motion_gnd, DOF_6=True)

                    exporter_til = Exporter(
                        bvh_name,
                        "decompressor_Ytil_" + str(idx_iter) + str(idx_sample) + ".bvh",
                    )
                    exporter_til.init_export(len(searched_motion_til))
                    exporter_til.export_motion(searched_motion_til, DOF_6=True)

                except IOError as e:
                    print(e)

    # TODO
    # Build batches respecting window size
    indices = []
    for i in range(n_frame - window):
        indices.append(np.arange(i, i + window))
    indices = torch.as_tensor(np.array(indices), dtype=torch.long)

    # Train

    writer = SummaryWriter()

    optimizer = torch.optim.AdamW(
        list(network_compressor.parameters()) + list(network_decompressor.parameters()),
        lr=lr,
        amsgrad=True,
        weight_decay=0.001,
    )

    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.99)

    rolling_loss = None

    sys.stdout.write("\n")

    for i in range(n_iter):
        optimizer.zero_grad()

        # Extract batch

        batch = indices[torch.randint(0, len(indices), size=[batch_size])]

        Xgnd = X[batch]

        Ygnd_pos = Ypos[batch]
        Ygnd_txy = Ytxy[batch]
        Ygnd_vel = Yvel[batch]
        Ygnd_ang = Yang[batch]

        Qgnd_pos = Qpos[batch]
        Qgnd_xfm = Qxfm[batch]
        Qgnd_txy = Qtxy[batch]
        Qgnd_vel = Qvel[batch]
        Qgnd_ang = Qang[batch]

        # Ygnd_rvel = Yrvel[batch]
        # Ygnd_rang = Yrang[batch]

        # Encode

        Zgnd = network_compressor(
            (
                torch.cat(
                    [
                        Ygnd_pos[:, :, 1:].reshape([batch_size, window, -1]),
                        Ygnd_txy[:, :, 1:].reshape([batch_size, window, -1]),
                        Ygnd_vel[:, :, 1:].reshape([batch_size, window, -1]),
                        Ygnd_ang[:, :, 1:].reshape([batch_size, window, -1]),
                        Qgnd_pos[:, :, 1:].reshape([batch_size, window, -1]),
                        Qgnd_txy[:, :, 1:].reshape([batch_size, window, -1]),
                        Qgnd_vel[:, :, 1:].reshape([batch_size, window, -1]),
                        Qgnd_ang[:, :, 1:].reshape([batch_size, window, -1]),
                        # Ygnd_rvel.reshape([batch_size, window, -1]),
                        # Ygnd_rang.reshape([batch_size, window, -1]),
                    ],
                    dim=-1,
                )
                - compressor_mean_in
            )
            / compressor_std_in
        )

        # Decode

        Ytil = (
            network_decompressor(torch.cat([Xgnd, Zgnd], dim=-1)) * decompressor_std_out
            + decompressor_mean_out
        )

        Ytil_pos = Ytil[:, :, 0 * (n_joint - 1) : 3 * (n_joint - 1)].reshape(
            [batch_size, window, n_joint - 1, 3]
        )
        Ytil_txy = Ytil[:, :, 3 * (n_joint - 1) : 9 * (n_joint - 1)].reshape(
            [batch_size, window, n_joint - 1, 3, 2]
        )
        Ytil_vel = Ytil[:, :, 9 * (n_joint - 1) : 12 * (n_joint - 1)].reshape(
            [batch_size, window, n_joint - 1, 3]
        )
        Ytil_ang = Ytil[:, :, 12 * (n_joint - 1) : 15 * (n_joint - 1)].reshape(
            [batch_size, window, n_joint - 1, 3]
        )
        # Ytil_rvel = Ytil[:, :, 15 * (n_joint - 1) + 0 : 15 * (n_joint - 1) + 3].reshape(
        #     [batch_size, window, 3]
        # )
        # Ytil_rang = Ytil[:, :, 15 * (n_joint - 1) + 3 : 15 * (n_joint - 1) + 6].reshape(
        #     [batch_size, window, 3]
        # )

        # Add root bone from ground

        Ytil_pos = torch.cat([Ygnd_pos[:, :, 0:1], Ytil_pos], dim=2)
        Ytil_txy = torch.cat([Ygnd_txy[:, :, 0:1], Ytil_txy], dim=2)
        Ytil_vel = torch.cat([Ygnd_vel[:, :, 0:1], Ytil_vel], dim=2)
        Ytil_ang = torch.cat([Ygnd_ang[:, :, 0:1], Ytil_ang], dim=2)

        # Do FK

        Ytil_xfm = txform.from_xy(Ytil_txy)

        Gtil_xfm, Gtil_pos, Gtil_vel, Gtil_ang = txform.fk_vel(
            Ytil_xfm, Ytil_pos, Ytil_vel, Ytil_ang, parents
        )

        # Compute Character Space

        Qtil_xfm = txform.inv_mul(Gtil_xfm[:, :, 0:1], Gtil_xfm)
        Qtil_pos = txform.inv_mul_vec(
            Gtil_xfm[:, :, 0:1], Gtil_pos - Gtil_pos[:, :, 0:1]
        )
        Qtil_vel = txform.inv_mul_vec(Gtil_xfm[:, :, 0:1], Gtil_vel)
        Qtil_ang = txform.inv_mul_vec(Gtil_xfm[:, :, 0:1], Gtil_ang)

        # Compute deltas

        Ygnd_dpos = (Ygnd_pos[:, 1:] - Ygnd_pos[:, :-1]) / frame_time
        Ygnd_drot = (Ygnd_txy[:, 1:] - Ygnd_txy[:, :-1]) / frame_time
        Qgnd_dpos = (Qgnd_pos[:, 1:] - Qgnd_pos[:, :-1]) / frame_time
        Qgnd_drot = (Qgnd_xfm[:, 1:] - Qgnd_xfm[:, :-1]) / frame_time

        Ytil_dpos = (Ytil_pos[:, 1:] - Ytil_pos[:, :-1]) / frame_time
        Ytil_drot = (Ytil_txy[:, 1:] - Ytil_txy[:, :-1]) / frame_time
        Qtil_dpos = (Qtil_pos[:, 1:] - Qtil_pos[:, :-1]) / frame_time
        Qtil_drot = (Qtil_xfm[:, 1:] - Qtil_xfm[:, :-1]) / frame_time

        Zdgnd = (Zgnd[:, 1:] - Zgnd[:, :-1]) / frame_time

        # Compute losses

        loss_loc_pos = torch.mean(75.0 * torch.abs(Ygnd_pos - Ytil_pos))
        loss_loc_txy = torch.mean(10.0 * torch.abs(Ygnd_txy - Ytil_txy))
        loss_loc_vel = torch.mean(10.0 * torch.abs(Ygnd_vel - Ytil_vel))
        loss_loc_ang = torch.mean(1.25 * torch.abs(Ygnd_ang - Ytil_ang))
        # loss_loc_rvel = torch.mean(2.0 * torch.abs(Ygnd_rvel - Ytil_rvel))
        # loss_loc_rang = torch.mean(2.0 * torch.abs(Ygnd_rang - Ytil_rang))

        loss_chr_pos = torch.mean(15.0 * torch.abs(Qgnd_pos - Qtil_pos))
        loss_chr_xfm = torch.mean(5.0 * torch.abs(Qgnd_xfm - Qtil_xfm))
        loss_chr_vel = torch.mean(2.0 * torch.abs(Qgnd_vel - Qtil_vel))
        loss_chr_ang = torch.mean(1.75 * torch.abs(Qgnd_ang - Qtil_ang))

        loss_lvel_pos = torch.mean(10.0 * torch.abs(Ygnd_dpos - Ytil_dpos) * 5)
        loss_lvel_rot = torch.mean(1.75 * torch.abs(Ygnd_drot - Ytil_drot) * 5)
        loss_cvel_pos = torch.mean(2.0 * torch.abs(Qgnd_dpos - Qtil_dpos) * 5)
        loss_cvel_rot = torch.mean(0.75 * torch.abs(Qgnd_drot - Qtil_drot) * 5)

        loss_sreg = torch.mean(0.1 * torch.abs(Zgnd))
        loss_lreg = torch.mean(0.1 * torch.square(Zgnd))
        loss_vreg = torch.mean(0.01 * torch.abs(Zdgnd))

        loss = (
            loss_loc_pos
            + loss_loc_txy
            + loss_loc_vel
            + loss_loc_ang
            # + loss_loc_rvel
            # + loss_loc_rang
            + loss_chr_pos
            + loss_chr_xfm
            + loss_chr_vel
            + loss_chr_ang
            + loss_lvel_pos
            + loss_lvel_rot
            + loss_cvel_pos
            + loss_cvel_rot
            + loss_sreg
            + loss_lreg
            + loss_vreg
        )

        # Backprop

        loss.backward()

        optimizer.step()

        # Logging

        writer.add_scalar("decompressor/loss", loss.item(), i)

        writer.add_scalars(
            "decompressor/loss_terms",
            {
                "loc_pos": loss_loc_pos.item(),
                "loc_txy": loss_loc_txy.item(),
                "loc_vel": loss_loc_vel.item(),
                "loc_ang": loss_loc_ang.item(),
                # "loc_rvel": loss_loc_rvel.item(),
                # "loc_rang": loss_loc_rang.item(),
                "chr_pos": loss_chr_pos.item(),
                "chr_xfm": loss_chr_xfm.item(),
                "chr_vel": loss_chr_vel.item(),
                "chr_ang": loss_chr_ang.item(),
                "lvel_pos": loss_lvel_pos.item(),
                "lvel_rot": loss_lvel_rot.item(),
                "cvel_pos": loss_cvel_pos.item(),
                "cvel_rot": loss_cvel_rot.item(),
                "sreg": loss_sreg.item(),
                "lreg": loss_lreg.item(),
                "vreg": loss_vreg.item(),
            },
            i,
        )

        writer.add_scalars(
            "decompressor/latent",
            {
                "mean": Zgnd.mean().item(),
                "std": Zgnd.std().item(),
            },
            i,
        )

        if rolling_loss is None:
            rolling_loss = loss.item()
        else:
            rolling_loss = rolling_loss * 0.99 + loss.item() * 0.01

        # if i % 100 == 0:
        if i % 1000 == 0:
            sys.stdout.write("\rIter: %7i Loss: %5.3f" % (i, rolling_loss))

        if i % 50000 == 0:
            # if i % 500 == 0:
            if args.save_sample:
                generate_animation(i)

            if args.save_model:
                save_compressed_database(
                    network_compressor,
                    [Ypos, Ytxy, Yvel, Yang, Qpos, Qtxy, Qvel, Qang],
                    n_frame,
                    compressor_mean_in,
                    compressor_std_in,
                    feature_database,
                )
                torch.save(network_decompressor.state_dict(), "decompressor.pt")
                torch.save(network_compressor.state_dict(), "compressor.pt")
                np.save("decompressor_mean_out.npy", decompressor_mean_out)
                np.save("decompressor_std_out.npy", decompressor_std_out)
                np.save("compressor_mean_in.npy", compressor_mean_in)
                np.save("compressor_std_in.npy", compressor_std_in)

        if i % 1000 == 0:
            scheduler.step()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Path
    parser.add_argument(
        "--bvh_name",
        type=str,
        default="data/matching_data/rhythm_motion/VAAI_Short_01_02.bvh",
    )
    parser.add_argument(
        "--bvh_npz_path", type=str, default="data/matching_data/rhythm_motion_npz/"
    )
    parser.add_argument(
        "--audio_db_path", type=str, default="data/matching_data/rhythm_audio"
    )
    parser.add_argument(
        "--silent_db_path", type=str, default="data/matching_data/silent_release"
    )
    parser.add_argument(
        "--test_audio_path", type=str, default="data/audio/Test/TTS_Hi.wav"
    )

    parser.add_argument(
        "--motion_type", type=str, default="gesture", choices=["gesture, silent"]
    )

    # Train
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--n_iter", type=int, default=1000000)  # 500000
    parser.add_argument("--window", type=int, default=10)
    parser.add_argument("--frame_time", type=float, default=0.0166667)

    # Motion
    parser.add_argument("--n_joint", type=int, default=61)
    parser.add_argument("--n_latent", type=int, default=64)
    parser.add_argument("--frame_size", type=int, default=300)

    # Save, Debug
    parser.add_argument("--save_model", type=bool, default=True)
    parser.add_argument("--save_sample", type=bool, default=True)
    parser.add_argument("--n_sample", type=int, default=10)

    args = parser.parse_args()
    main(args)


##########################
# Write BVH Test
# Write BVH
# frames_output = []
# local_transforms = get_local_transform_from_posrot(Ypos[:71], Yrot[:71])
# for idx_frame in range(71):
#     frames_output.append(Frame(skeleton, motion_database.get_motion(0)[0].get_root_transform(), local_transforms[idx_frame]))
#     # frames_output.append(Frame(skeleton, local_transforms[idx_frame][0], local_transforms[idx_frame]))

# searched_motion = Motion(skeleton, frames_output, frame_time)
# exporter = Exporter(
#     bvh_name, "restore_test.bvh"
# )
# exporter.init_export(len(searched_motion))
# exporter.export_motion(searched_motion, DOF_6=True)


# searched_motion = motion_database.get_motion(0)
# exporter = Exporter(
#     bvh_name, "restore_gnd.bvh"
# )
# exporter.init_export(len(searched_motion))
# exporter.export_motion(searched_motion, DOF_6=True)

# exit()
