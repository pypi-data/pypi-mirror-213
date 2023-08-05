import os
import pickle
import time
from pathlib import Path
from typing import Optional

import numpy as np
from parameter.gesture_matching_parameter import MCS_LOWER_BLENDING
from tqdm import tqdm
from utilities.utils import get_data_stats, normalize_data

from core.audio import Audio, AudioDatabase
from core.feature import (AudioFeature, HeadPoseFeature, LowerPoseFeature,
                          NonTalkingPoseFeature, WeightedUpperVelFeature)
from core.motion import MotionDatabase


class AudioFeatureDatabase:
    def __init__(self, audio: Audio, fps):
        start_time = time.time()
        self._audio = audio
        self._is_loaded = False
        self.fps = round(fps)
        self.time_delta = 2

        self.motion_look_ahead = range(0, 8 * self.time_delta, self.time_delta)
        self.audio_look_ahead = range(0, self.fps, self.time_delta)
        self.beat_look_ahead = range(0, self.fps)
        """
        Don't include 0 in beat_look_behind
        Note that beat_look_behind goes in a descending order!
        Ex: 
        If you don't want look behind, set beat_look_behind = []
        """
        self.beat_look_behind = []
        self._audio_feature = AudioFeature(
            beat_look_ahead=self.beat_look_ahead,
            beat_look_behind=self.beat_look_behind,
            aud_feat_idx=self.audio_look_ahead,
        )
        self._mfcc_feature_size = self._audio_feature.mfcc_dof
        self._beat_feature_size = self._audio_feature.beat_dof
        # generate matching db
        self._is_loaded = self.preprocess_from_scratch()
        if self._is_loaded:
            print("Test Audio initialization", time.time() - start_time)

    @property
    def is_loaded(self):
        return self._is_loaded

    def preprocess_from_scratch(
        self,
    ):
        mfcc_mean, mfcc_std = get_data_stats(self._audio.mfcc())
        norm_mfcc = normalize_data(self._audio.mfcc(), mfcc_mean, mfcc_std)
        self.mfcc_feature = self._audio_feature.compute_mfcc_feature(norm_mfcc)[:, :]
        self.beat_feature = self._audio_feature.compute_beat_feature(
            self._audio.beat()
        )[:, :]
        return True


class MotionFeatureDatabase:
    def __init__(
        self,
        motion_db: MotionDatabase,
        db_path: str = "data/matching_data",
        db_file_name="wv_silent_release.pickle",
    ):
        self._motion_db = motion_db
        self._skel = motion_db._skeleton
        self._db_path = db_path
        self._frame_time = motion_db.get_motion(0).frame_time
        self._is_loaded = False

        self.fps = round(1.0 / self._frame_time)
        self.time_delta = 2
        self._control_weight = 1.4

        self.motion_look_ahead = range(0, 8 * self.time_delta, self.time_delta)

        self.pose_feature = []
        self.head_feature = []
        self.lower_feature = []

        self.idx_motion_list = []
        self.motion_name_list = []

        # generate matching db
        self.db_file_name = db_file_name
        self._is_loaded = self.preprocess_from_pickle_file()
        if self._is_loaded:
            pass
        else:
            self._is_loaded = self.preprocess_from_scratch()

    @property
    def is_loaded(self):
        return self._is_loaded

    def get_search_weight(self):
        weights = self._pose_feature.get_weights()
        weights["control"] = self._control_weight
        return weights

    def set_search_weight(self, weights):
        self._control_weight = weights.pop("control")
        self._pose_feature.set_weights(weights)

    def preprocess_from_pickle_file(
        self,
    ):
        if os.path.exists(self._db_path):
            path = "{}/{}".format(self._db_path, self.db_file_name)
            if os.path.exists(path):
                with open(path, "rb") as fr:
                    db = pickle.load(fr)
                    self.idx_motion_list = db["idx_motion_list"]
                    n_feature = len(db["pose_feature"])
                    for idx_feature in range(n_feature):
                        self.pose_feature.append(db["pose_feature"][idx_feature])
                        self.lower_feature.append(db["lower_feature"][idx_feature])
                        self.head_feature.append(db["head_feature"][idx_feature])
            else:
                return False
        self.calc_nums()

        return True

    def preprocess_from_scratch(
        self,
    ):
        _pose_feature = WeightedUpperVelFeature(look_ahead=self.motion_look_ahead)
        _head_feature = HeadPoseFeature(look_ahead=self.motion_look_ahead)
        _lower_feature = LowerPoseFeature(look_ahead=self.motion_look_ahead)

        self._pose_feature_size = _pose_feature.dof
        self._lower_feature_size = _lower_feature.dof
        self._head_feature_size = _head_feature.dof

        for idx_motion in range(self._motion_db.num_motion()):
            motion = self._motion_db.get_motion(idx_motion)
            self.idx_motion_list.append(idx_motion)
            lower_feature = _lower_feature.compute_feature(motion)
            pose_feature = _pose_feature.compute_feature(motion)
            head_feature = _head_feature.compute_feature(motion)

            pose_feature = np.expand_dims(pose_feature, axis=0)
            lower_feature = np.expand_dims(lower_feature, axis=0)
            head_feature = np.expand_dims(head_feature, axis=0)
            self.pose_feature.append(pose_feature)
            self.lower_feature.append(lower_feature)
            self.head_feature.append(head_feature)

        self.save_db()
        self.calc_nums()
        return True

    def save_db(
        self,
    ):
        db_dict = {
            "idx_motion_list": [],
            "pose_feature": [],
            "lower_feature": [],
            "head_feature": [],
        }

        for idx_feature in range(len(self.pose_feature)):
            db_dict["pose_feature"].append(self.pose_feature[idx_feature])
            db_dict["lower_feature"].append(self.lower_feature[idx_feature])
            db_dict["head_feature"].append(self.head_feature[idx_feature])
        db_dict["idx_motion_list"] = self.idx_motion_list
        save_filename = "{}/{}".format(self._db_path, self.db_file_name)
        with open(save_filename, "wb") as fw:
            pickle.dump(db_dict, fw)

    def calc_nums(
        self,
    ):
        self._num_motion = len(self.pose_feature)
        self._num_seq = 1
        self._num_frame = []
        for pose_feature_motion in self.pose_feature:
            self._num_frame.append(pose_feature_motion[0].shape[1])

    def get_motion(self, idx_motion):
        return self._motion_db.get_motion(self.idx_motion_list[idx_motion])

    def get_frame(self, idx_motion, frame_idx):
        return self._motion_db.get_frame(self.idx_motion_list[idx_motion], frame_idx)

    def get_sliced_frame(self, idx_motion, i, j):
        return self._motion_db.get_frame(self.idx_motion_list[idx_motion], 0 * i + j)


class MotionAudioFeatureDatabase:
    def __init__(
        self,
        motion_db: MotionDatabase,
        audio_db: Optional[AudioDatabase] = None,
        slice: bool = True,
        control_weight: float = 1.4,
        frame_size: int = 300,
        db_path: str = "data/matching_data",
        db_file_name: str = "wv_feature.pickle",
    ):
        start_time = time.time()
        self._motion_db = motion_db
        self._skel = motion_db._skeleton
        self._db_path = Path(db_path)
        self._frame_time = motion_db.get_motion(0).frame_time
        self._audio_db = audio_db
        self.slice = slice
        self.frame_size = frame_size
        self._is_loaded = False

        self.fps = round(1.0 / self._frame_time)
        self.time_delta = 2
        self._control_weight = control_weight

        # look_ahead: 반영할 미래 정보에 대한 idx list
        self.motion_look_ahead = range(0, 8 * self.time_delta, self.time_delta)
        self.audio_look_ahead = range(0, self.fps, self.time_delta)
        self.beat_look_ahead = range(0, self.fps)
        self.beat_look_behind = []

        """
        Don't include 0 in beat_look_behind
        Note that beat_look_behind goes in a descending order!
        Ex: self.beat_look_behind = range(10,0,-1)
        If you don't want look behind, set beat_look_behind = []
        """
        self._head_base = "Neck"
        self.lower_joints_matching = MCS_LOWER_BLENDING

        self.pose_feature = []
        self.lower_feature = []
        self.head_feature = []
        self.mfcc_feature = []
        self.beat_feature = []

        self.idx_motion_list = []
        self.motion_name_list = []
        self.db_file_name = db_file_name

        if os.path.exists(self._db_path / self.db_file_name):
            self._is_loaded = self.preprocess_from_pickle_file()

        if not self._is_loaded:
            self._is_loaded = self.preprocess_from_scratch()

        if self._is_loaded:
            print("Matching database initialization:", time.time() - start_time)
        else:
            print("Matching database initialization failed")

    @property
    def head_base(self):
        return self._head_base

    @property
    def is_loaded(self):
        return self._is_loaded

    def get_search_weight(self):
        weights = self._pose_feature.get_weights()
        weights["control"] = self._control_weight
        return weights

    def set_search_weight(self, weights):
        self._control_weight = weights.pop("control")
        self._pose_feature.set_weights(weights)

    """
    Here, since we are dealing with both motion and the audio data,
    we need to make sure that the motion data is properly paired with the audio data
    To do so, we get the name of the audio_db and compare it with the motion_db's file path
    """

    def preprocess_from_pickle_file(
        self,
    ):
        print("Load data from preprocess_from_scratched file:", self.db_file_name)
        pickle_file_path = self._db_path / self.db_file_name
        try:
            with open(pickle_file_path, "rb") as fr:
                db = pickle.load(fr)
                self.idx_motion_list = db["idx_motion_list"]
                self.motion_name_list = db["motion_name_list"]
                n_feature = len(db["pose_feature"])
                for idx_feature in range(n_feature):
                    self.pose_feature.append(db["pose_feature"][idx_feature])
                    self.lower_feature.append(db["lower_feature"][idx_feature])
                    self.head_feature.append(db["head_feature"][idx_feature])
                    self.mfcc_feature.append(db["mfcc_feature"][idx_feature])
                    self.beat_feature.append(db["beat_feature"][idx_feature])
            self.calc_nums()

            self._pose_feature_size = self.pose_feature[0].shape[2]
            self._lower_feature_size = self.lower_feature[0].shape[2]
            self._head_feature_size = self.head_feature[0].shape[2]
            self._mfcc_feature_size = self.mfcc_feature[0].shape[2]
            self._beat_feature_size = self.beat_feature[0].shape[2]
            return True

        except Exception:
            return False

    def preprocess_from_scratch(
        self,
    ):
        """
        Gesture feature DB is the list of
        [pose_feature, mfcc_feature, beat_feature]
        If it is sliced, the features are reshaped to
        ((-1, self.frame_size, feature_size))
        Otherwies, ((1, total_len, feature_size))
        """
        print("Preprocessing from a scratch")

        _pose_feature = WeightedUpperVelFeature(look_ahead=self.motion_look_ahead)
        _head_feature = HeadPoseFeature(look_ahead=self.motion_look_ahead)
        _lower_feature = LowerPoseFeature(look_ahead=self.motion_look_ahead)
        _audio_feature = AudioFeature(
            beat_look_ahead=self.beat_look_ahead,
            beat_look_behind=self.beat_look_behind,
            aud_feat_idx=self.audio_look_ahead,
        )
        self._pose_feature_size = _pose_feature.dof
        self._lower_feature_size = _lower_feature.dof
        self._head_feature_size = _head_feature.dof
        self._mfcc_feature_size = _audio_feature.mfcc_dof
        self._beat_feature_size = _audio_feature.beat_dof

        for a_num in tqdm(range(self._audio_db.num_audio())):
            audio = self._audio_db.get_audio(a_num)
            file_name = audio._name
            unpacked = self._motion_db.get_idx_motion_by_name(file_name)
            if unpacked is None:
                print("The audio {} has no mathcing motion".format(file_name))
                continue
            else:
                idx_motion, motion = unpacked[0], unpacked[1]
                self.motion_name_list.append(file_name)
                self.idx_motion_list.append(idx_motion)

                pose_feature = _pose_feature.compute_feature(motion)
                lower_feature = _lower_feature.compute_feature(motion)
                head_feature = _head_feature.compute_feature(motion)

                norm_mfcc = normalize_data(
                    audio.mfcc(), self._audio_db.mfcc_mean, self._audio_db.mfcc_std
                )
                mfcc_feature = _audio_feature.compute_mfcc_feature(norm_mfcc)[:, :]
                beat_feature = _audio_feature.compute_beat_feature(audio.beat())[:, :]

                # Pad
                if mfcc_feature.shape[0] < pose_feature.shape[0]:
                    mfcc_feature = np.pad(
                        mfcc_feature,
                        ((0, pose_feature.shape[0] - mfcc_feature.shape[0]), (0, 0)),
                        "constant",
                        constant_values=0,
                    )
                if beat_feature.shape[0] < pose_feature.shape[0]:
                    beat_feature = np.pad(
                        beat_feature,
                        ((0, pose_feature.shape[0] - beat_feature.shape[0]), (0, 0)),
                        "constant",
                        constant_values=0,
                    )

                if self.slice:
                    num_len = pose_feature.shape[0] // self.frame_size
                    pose_feature = pose_feature[: num_len * self.frame_size]
                    lower_feature = lower_feature[: num_len * self.frame_size]
                    head_feature = head_feature[: num_len * self.frame_size]
                    mfcc_feature = mfcc_feature[: num_len * self.frame_size]
                    beat_feature = beat_feature[: num_len * self.frame_size]
                    # slice
                    pose_feature = pose_feature.reshape(
                        (-1, self.frame_size, self._pose_feature_size)
                    )
                    lower_feature = lower_feature.reshape(
                        (-1, self.frame_size, self._lower_feature_size)
                    )
                    head_feature = head_feature.reshape(
                        (-1, self.frame_size, self._head_feature_size)
                    )
                    mfcc_feature = mfcc_feature.reshape(
                        (-1, self.frame_size, self._mfcc_feature_size)
                    )
                    beat_feature = beat_feature.reshape(
                        (-1, self.frame_size, self._beat_feature_size)
                    )

                    use_train = False  # TODO
                    if not use_train:
                        # Since the end part of the step_size is not used in this case, we should put redundant data
                        for i in range(num_len - 1):
                            mo_temp_feature = np.zeros(
                                (1, self.frame_size, self._pose_feature_size)
                            )
                            mo_temp_feature[
                                0, : self.frame_size - self.frame_size // 2, :
                            ] = pose_feature[i, self.frame_size // 2 :, :]
                            mo_temp_feature[
                                0, self.frame_size - self.frame_size // 2 :, :
                            ] = pose_feature[i + 1, : self.frame_size // 2, :]
                            pose_feature = np.concatenate(
                                (pose_feature, mo_temp_feature), axis=0
                            )
                            lo_temp_feature = np.zeros(
                                (1, self.frame_size, self._lower_feature_size)
                            )
                            lo_temp_feature[
                                0, : self.frame_size - self.frame_size // 2, :
                            ] = lower_feature[i, self.frame_size // 2 :, :]
                            lo_temp_feature[
                                0, self.frame_size - self.frame_size // 2 :, :
                            ] = lower_feature[i + 1, : self.frame_size // 2, :]
                            lower_feature = np.concatenate(
                                (lower_feature, lo_temp_feature), axis=0
                            )
                            hd_temp_feature = np.zeros(
                                (1, self.frame_size, self._head_feature_size)
                            )
                            hd_temp_feature[
                                0, : self.frame_size - self.frame_size // 2, :
                            ] = head_feature[i, self.frame_size // 2 :, :]
                            hd_temp_feature[
                                0, self.frame_size - self.frame_size // 2 :, :
                            ] = head_feature[i + 1, : self.frame_size // 2, :]
                            head_feature = np.concatenate(
                                (head_feature, hd_temp_feature), axis=0
                            )
                            mf_temp_feature = np.zeros(
                                (1, self.frame_size, self._mfcc_feature_size)
                            )
                            mf_temp_feature[
                                0, : self.frame_size - self.frame_size // 2, :
                            ] = mfcc_feature[i, self.frame_size // 2 :, :]
                            mf_temp_feature[
                                0, self.frame_size - self.frame_size // 2 :, :
                            ] = mfcc_feature[i + 1, : self.frame_size // 2, :]
                            mfcc_feature = np.concatenate(
                                (mfcc_feature, mf_temp_feature), axis=0
                            )
                            bt_temp_feature = np.zeros(
                                (1, self.frame_size, self._beat_feature_size)
                            )
                            bt_temp_feature[
                                0, : self.frame_size - self.frame_size // 2, :
                            ] = beat_feature[i, self.frame_size // 2 :, :]
                            bt_temp_feature[
                                0, self.frame_size - self.frame_size // 2 :, :
                            ] = beat_feature[i + 1, : self.frame_size // 2, :]
                            beat_feature = np.concatenate(
                                (beat_feature, bt_temp_feature), axis=0
                            )

                else:
                    pose_feature = np.expand_dims(pose_feature, axis=0)
                    lower_feature = np.expand_dims(lower_feature, axis=0)
                    head_feature = np.expand_dims(head_feature, axis=0)
                    mfcc_feature = np.expand_dims(mfcc_feature, axis=0)
                    beat_feature = np.expand_dims(beat_feature, axis=0)
                self.pose_feature.append(pose_feature)
                self.lower_feature.append(lower_feature)
                self.head_feature.append(head_feature)
                self.mfcc_feature.append(mfcc_feature)
                self.beat_feature.append(beat_feature)
        self.save_db()
        self.calc_nums()
        return True

    def save_db(
        self,
    ):
        """
        save feature information in pickle file
        """
        db_dict = {
            "idx_motion_list": [],
            "motion_name_list": [],
            "pose_feature": [],
            "mfcc_feature": [],
            "beat_feature": [],
            "lower_feature": [],
            "head_feature": [],
        }
        for idx_feature in range(len(self.pose_feature)):
            db_dict["pose_feature"].append(self.pose_feature[idx_feature])
            db_dict["lower_feature"].append(self.lower_feature[idx_feature])
            db_dict["head_feature"].append(self.head_feature[idx_feature])
            db_dict["mfcc_feature"].append(self.mfcc_feature[idx_feature])
            db_dict["beat_feature"].append(self.beat_feature[idx_feature])
        db_dict["idx_motion_list"] = self.idx_motion_list
        db_dict["motion_name_list"] = self.motion_name_list
        save_filename = "{}/{}".format(self._db_path, self.db_file_name)
        with open(save_filename, "wb") as fw:
            pickle.dump(db_dict, fw)
        print("DB saved")

    def calc_nums(
        self,
    ):
        self._num_motion = len(self.pose_feature)
        total = 0

        if self.slice:
            self._num_seq = []
            self._num_frame = self.frame_size
        else:
            self._num_seq = 1
            self._num_frame = []

        for pose_feature_motion in self.pose_feature:
            if self.slice:
                self._num_seq.append(pose_feature_motion.shape[0])
            else:
                self._num_frame.append(pose_feature_motion.shape[1])

    def get_motion(self, idx_motion):
        return self._motion_db.get_motion(self.idx_motion_list[idx_motion])

    def get_frame(self, idx_motion, idx_frame):
        return self._motion_db.get_frame(self.idx_motion_list[idx_motion], idx_frame)

    def get_sliced_frame(self, idx_motion, i, j):
        """
        Args
            motion_idx: motion idx
            i: seq idx
            j: frame idx
        Returns:

        """
        return self._motion_db.get_frame(
            self.idx_motion_list[idx_motion], self.frame_size * i + j
        )

    # DB 만들 때 augment 해서, 이렇게 찾아야 함
    def get_aug_sliced_frame(self, idx_motion, i, j):
        # return self.get_sliced_frame(idx_motion, i, j)
        mo_len = self._num_seq[idx_motion] // 2 + 1
        if mo_len > i:
            return self.get_sliced_frame(idx_motion, i, j)
        else:
            if self.frame_size - self.frame_size // 2 > j:
                new_i = i - mo_len
                new_j = j + self.frame_size // 2
            else:
                new_i = i + 1 - mo_len
                new_j = j - (self.frame_size - self.frame_size // 2)
            return self.get_sliced_frame(idx_motion, new_i, new_j)


class LatentFeatureDatabase:
    def __init__(
        self,
        path: str = "latentFeature.pickle",
        slice: bool = True,
        frame_size: int = 300,
    ):
        self.path = path
        self.slice = slice
        self.frame_size = frame_size
        self.latent_feature = []

        if os.path.exists(self.path):
            print("load db")
            self.load_db(self.path)
        else:
            raise FileNotFoundError

    def load_db(self, path: str):
        with open(path, "rb") as fr:
            self.latent_feature = pickle.load(fr)

    def get_sliced_frame(self, idx_motion, idx_seq, idx_frame):
        return self.latent_feature[idx_motion][idx_seq][idx_frame]


class DefaultMotionFeatureDatabase:
    def __init__(
        self,
        motion_db: MotionDatabase,
        feature: NonTalkingPoseFeature,
        motion_look_ahead: list,
        db_path="path/to/featuredb",
        db_file_name="motion_feature.pickle",
        *args
    ):
        """
        Default motino feature: Non-slice version
        motion_db: 기본 모션 db
        feature: 어떤 feature 사용할것인지
        motion_look_ahead: 모션을 얼마나 앞을 볼것인지
        db_path: feature db 저장 경로
        db_file_name: file name
        args: 추가 db (다른 db에서 추가적으로 feature를 구축하는 경우)
        """
        self._motion_db = motion_db
        self._skel = motion_db._skeleton
        self._db_path = db_path
        self._frame_time = motion_db.get_motion(0).frame_time
        self._is_loaded = False

        self.fps = round(1.0 / self._frame_time)
        self.time_del = 2
        self._control_weight = 1.4

        self.motion_look_ahead = motion_look_ahead
        self._pose_feature = feature
        self._pose_feature.update_look_ahead(self.motion_look_ahead)

        self._pose_feature_size = self._pose_feature.dof
        self.motion_idx_list = []

        for add_db in args:
            for motion_idx in range(add_db.num_motion()):
                self._motion_db.append_motion(add_db.get_motion(motion_idx))

        # generate matching db
        self.db_file_name = db_file_name
        self._is_loaded = self.preprocess_from_db()
        self.np_db = None
        if self._is_loaded:
            pass
        else:
            self._is_loaded = self.preprocess()

    @property
    def is_loaded(self):
        return self._is_loaded

    def get_search_weight(self):
        weights = self._pose_feature.get_weights()
        weights["control"] = self._control_weight
        return weights

    def set_search_weight(self, weights):
        self._control_weight = weights.pop("control")
        self._pose_feature.set_weights(weights)

    def preprocess_from_db(
        self,
    ):
        print("Load data from preprocess_from_scratched file:", self.db_file_name)
        self._gesture_feature_DB = []
        if os.path.exists(self._db_path):
            path = "{}/{}".format(self._db_path, self.db_file_name)
            if os.path.exists(path):
                with open(path, "rb") as fr:
                    db = pickle.load(fr)
                    self.motion_idx_list = db["motion_idx_list"]
                    n_db = len(db["pose_feature"])
                    for i in range(n_db):
                        self._gesture_feature_DB.append([db["pose_feature"][i]])
            else:
                return False
        self.calc_nums()
        return True

    def preprocess(
        self,
    ):
        self._gesture_feature_DB = []
        for idx_motion in tqdm(range(self._motion_db.num_motion())):
            motion = self._motion_db.get_motion(idx_motion)
            self.motion_idx_list.append(idx_motion)
            pose_feature = self._pose_feature.compute_feature(motion)
            pose_feature = np.expand_dims(pose_feature, axis=0)
            self._gesture_feature_DB.append([pose_feature])
        self.save_db()
        self.calc_nums()
        return True

    def save_db(
        self,
    ):
        db_dict = {"motion_idx_list": [], "pose_feature": []}
        for db in self._gesture_feature_DB:
            db_dict["pose_feature"].append(db[0])
        db_dict["motion_idx_list"] = self.motion_idx_list
        save_filename = "{}/{}".format(self._db_path, self.db_file_name)
        with open(save_filename, "wb") as fw:
            pickle.dump(db_dict, fw)

    def calc_nums(
        self,
    ):
        self._num_motion = len(self._gesture_feature_DB)
        self._num_seq = 1
        self._num_frame = []
        for db in self._gesture_feature_DB:
            self._num_frame.append(db[0].shape[1])

    def get_motion(self, motion_idx):
        return self._motion_db.get_motion(self.motion_idx_list[motion_idx])

    def get_frame(self, motion_idx, frame_idx):
        return self._motion_db.get_frame(self.motion_idx_list[motion_idx], frame_idx)

    def numpy_db(
        self,
    ):
        if self.np_db is None:
            dblist = []
            idxlist = []
            cnt = 0
            for i in range(len(self._gesture_feature_DB)):
                idxlist.append(cnt)
                cnt += len(self._gesture_feature_DB[i][0][0])
                for j in range(len(self._gesture_feature_DB[i][0][0])):
                    dblist.append(self._gesture_feature_DB[i][0][0][j])
            idxlist.append(cnt)
            self.np_db = np.array(dblist)
            self.idx_list = idxlist
        return self.np_db, self.idx_list
