import time

from vaaibody.core.audio import AudioDatabase, load_audio_from_wav
from vaaibody.core.database import (
    AudioFeatureDatabase,
    MotionAudioFeatureDatabase,
    MotionFeatureDatabase,
)
from vaaibody.core.gesture_matching import GestureMatching
from vaaibody.core.motion import MotionDatabase
from vaaibody.core.skeleton import Skeleton
from vaaibody.utilities.exporter import Exporter
from vaaibody.utilities.audio_utils import silent_detector
from vaaibody.viewer.gesture_result_viewer import GestureWindow
import pathlib

file_path = pathlib.Path(__file__).parent.resolve()
data_path = file_path.parent.parent / "data"


def match_gesture(
    bvh_name="/home/yoonhee/Downloads/221123_Body_KSW/Gesture_Before/VAAI_Basic_01_03.bvh",
    bvh_npz_path="data/matching_data/rhythm_motion_npz",
    audio_db_path="data/matching_data/rhythm_audio",
    silent_db_path="data/matching_data/silent_release",
    test_audio_path="data/audio/Test/TTS.wav",
):
    """
    Init Database, parameters
    """
    skeleton = Skeleton(name="KSW")
    skeleton.load_hierarchy_from_bvh(bvh_name)
    motion_db = MotionDatabase(skeleton, bvh_npz_path, use_npz=True)

    fps = round(1.0 / motion_db.get_frame_time())
    frame_size = round(fps) * 2
    step_size = round(round(fps) * 0.5)
    audio_db = AudioDatabase(audio_db_path, fps, from_path=True)
    gdb = MotionAudioFeatureDatabase(
        motion_db,
        audio_db,
        slice=False,
        frame_size=frame_size,
        db_path=data_path / "matching_data",
        db_file_name="wv_feature_no_sliced.pickle",
    )

    raw_silent_db = MotionDatabase(skeleton, silent_db_path, is_preload=True)
    silent_db = MotionFeatureDatabase(
        raw_silent_db,
        db_path=data_path / "matching_data",
        db_file_name="wv_silent_release.pickle",
    )
    """
    Gesture matching
    """
    gesture_matching = GestureMatching(gdb, step_size=step_size, silent_db=silent_db)
    test_audio = load_audio_from_wav(test_audio_path, frate=fps)
    test_db = AudioFeatureDatabase(test_audio, fps)
    _, sil_hint = silent_detector(
        test_db.mfcc_feature, std_thresh=-0.2, duration=round(1.0 * fps)
    )
    """
    Search Motion with silence hint
    """
    # gesture_matching.match_motion_with_silent(
    #     test_db.mfcc_feature.transpose(),
    #     test_db.beat_feature.transpose(),
    #     search_lower=False,
    #     sil_hint=sil_hint,
    # )

    gesture_matching.test_new_metric(
        test_db.beat_feature.transpose(),
        test_db.mfcc_feature.transpose(),
        sil_hint=sil_hint,
    )

    # gesture_matching.matching_head(filter="lowpass")
    searched_motion = gesture_matching.convert_frames()
    """
    Export and return results
    """
    timestr = time.strftime("%m%d_%H%M%S")
    # exporter = Exporter("data/matching_data/rhythm_motion/VAAI_Short_01_02.bvh", "data/matching_result/", "matching_result_" + timestr + ".bvh")
    exporter = Exporter(
        bvh_name,
        data_path / "matching_result" / str("matching_result_" + timestr + ".bvh"),
    )
    exporter.init_export(len(searched_motion))
    exporter.export_motion(searched_motion, DOF_6=True)
    return skeleton, searched_motion, test_audio, sil_hint


if __name__ == "__main__":
    skel, searched_motion, test_audio, sil_hint = match_gesture(
        bvh_name="/home/yoonhee/Downloads/221123_Body_KSW/Gesture_Before/VAAI_Basic_01_01.bvh",
        bvh_npz_path=data_path / "matching_data" / "rhythm_motion_npz",
        audio_db_path=data_path / "matching_data" / "rhythm_audio",
        silent_db_path=data_path / "matching_data" / "silent_release",
        test_audio_path=data_path / "audio" / "Test" / "TTS_Travel.wav",
    )
    print("Audio length: ", test_audio.audio().shape[0] / test_audio.sr())
    visualize = True
    if visualize:
        main_window = GestureWindow(skel, searched_motion, test_audio, sil_hint)
        main_window.loop()
