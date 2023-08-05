import time

import torch

from vaaibody.core.audio import *
from vaaibody.core.database import *
from vaaibody.core.gesture_matching import *
from vaaibody.core.motion import MotionDatabase
from vaaibody.core.skeleton import Skeleton
from vaaibody.utilities.audio_utils import silent_detector
import pathlib
from vaaibody.utilities.exporter import Exporter
from vaaibody.viewer.gesture_result_viewer import GestureWindow

file_path = pathlib.Path(__file__).parent.resolve()
data_path = file_path.parent.parent / "data"


def match_gesture(
    bvh_name="data/matching_data/rhythm_motion/VAAI_Short_01_02.bvh",
    bvh_npz_path="data/matching_data/rhythm_motion_npz/",
    audio_db_path="data/matching_data/rhythm_audio",
    silent_db_path="data/matching_data/silent_release",
    test_audio_path="data/audio/Test/TTS_Hi.wav",
):
    """
    Init Database, parameters
    """
    skeleton = Skeleton(name="KSW")
    skeleton.load_hierarchy_from_bvh(bvh_name)
    motion_db = MotionDatabase(skeleton, bvh_npz_path, use_npz=True)

    fps = round(1.0 / motion_db.get_frame_time())
    frame_size = round(fps) * 5  # 300
    step_size = round(round(fps) * 0.5)
    audio_db = AudioDatabase(audio_db_path, fps, from_path=True)
    gdb = MotionAudioFeatureDatabase(
        motion_db,
        audio_db,
        slice=True,
        frame_size=frame_size,
        db_path="data/matching_data",
        db_file_name="wv_feature_no_aug.pickle",
    )
    raw_silent_db = MotionDatabase(skeleton, silent_db_path, is_preload=True)
    silent_db = MotionFeatureDatabase(
        raw_silent_db, db_path=data_path / "matching_data"
    )

    ## NN
    # neural network
    n_features = gdb._pose_feature_size
    n_latent = 64
    latent_feature_db = LatentFeatureDatabase(
        path="latentFeature.pickle", slice=True, frame_size=30
    )

    from decompressor import Decompressor

    decompressor_mean_out = np.load("decompressor_mean_out.npy")
    decompressor_std_out = np.load("decompressor_std_out.npy")

    network_decompressor = Decompressor(
        n_features + n_latent, len(decompressor_mean_out)
    )
    network_decompressor.load_state_dict(torch.load("decompressor.pt"))
    network_decompressor.eval()

    gesture_matching = GestureMatching(
        gdb,
        step_size=step_size,
        silent_db=silent_db,
        latent_db=latent_feature_db,
        decompressor=network_decompressor,
        decompressor_mean_out=decompressor_mean_out,
        decompressor_std_out=decompressor_std_out,
    )

    """
    Gesture matching
    """
    test_audio = load_audio_from_wav(test_audio_path, frate=fps)
    test_db = AudioFeatureDatabase(test_audio, fps)
    _, sil_hint = silent_detector(
        test_db.mfcc_feature, std_thresh=-0.2, duration=round(1.0 * fps)
    )

    """
    Search Motion with silence hint
    """
    gesture_matching.match_motion_with_silent(
        test_db.mfcc_feature.transpose(),
        test_db.beat_feature.transpose(),
        search_lower=False,
        sil_hint=sil_hint,
    )
    # gesture_matching.matching_head(filter="lowpass")
    searched_motion = gesture_matching.convert_frames()

    """
    Export and return results
    """
    timestr = time.strftime("%m%d_%H%M%S")
    exporter = Exporter(
        bvh_name,
        data_path / "matching_result" / str("matching_result_" + timestr + ".bvh"),
    )
    exporter.init_export(len(searched_motion))
    exporter.export_motion(searched_motion, DOF_6=True)

    return skeleton, searched_motion, test_audio, sil_hint


if __name__ == "__main__":
    skel, searched_motion, test_audio, sil_hint = match_gesture()
    print(test_audio.audio().shape[0] / test_audio.sr())
    visualize = True
    if visualize:
        main_window = GestureWindow(skel, searched_motion, test_audio, sil_hint)
        main_window.loop()
