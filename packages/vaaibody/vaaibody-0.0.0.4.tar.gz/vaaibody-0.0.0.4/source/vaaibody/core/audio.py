"""
The mfcc code is the modification of the sphinx library
"""
import math
import os
import pickle
import time
from copy import deepcopy

import librosa
import natsort
import numpy as np
import numpy.fft
from tqdm import tqdm
from utilities.utils import *


def mel(f):
    return 2595.0 * numpy.log10(1.0 + f / 700.0)


def melinv(m):
    return 700.0 * (numpy.power(10.0, m / 2595.0) - 1.0)


def s2dctmat(nfilt, ncep, freqstep):
    melcos = numpy.empty((ncep, nfilt), "double")
    for i in range(0, ncep):
        freq = numpy.pi * float(i) / nfilt
        melcos[i] = numpy.cos(
            freq * numpy.arange(0.5, float(nfilt) + 0.5, 1.0, "double")
        )
    melcos[:, 0] = melcos[:, 0] * 0.5
    return melcos


class MFCC(object):
    def __init__(
        self,
        nfilt=40,
        ncep=13,
        lowerf=133.3333,
        upperf=6855.4976,
        alpha=0.97,
        samprate=16000,
        frate=100,
        wlen=0.0256,
        nfft=512,
    ):
        # Store parameters
        self.lowerf = lowerf
        self.upperf = upperf
        self.nfft = nfft
        self.ncep = ncep
        self.nfilt = nfilt
        self.frate = frate
        self.fshift = float(samprate) / frate

        # Build Hamming window
        self.wlen = int(wlen * samprate)
        self.win = numpy.hamming(self.wlen)

        # Prior sample for pre-emphasis
        self.prior = 0
        self.alpha = alpha

        # Build mel filter matrix
        self.filters = numpy.zeros((nfft // 2 + 1, nfilt), "d")
        dfreq = float(samprate) / nfft
        if upperf > samprate / 2:
            raise (
                Exception,
                "Upper frequency %f exceeds Nyquist %f" % (upperf, samprate / 2),
            )
        melmax = mel(upperf)
        melmin = mel(lowerf)
        dmelbw = (melmax - melmin) / (nfilt + 1)
        # Filter edges, in Hz
        filt_edge = melinv(melmin + dmelbw * numpy.arange(nfilt + 2, dtype="d"))

        for whichfilt in range(0, nfilt):
            # Filter triangles, in DFT points
            leftfr = round(filt_edge[whichfilt] / dfreq)
            centerfr = round(filt_edge[whichfilt + 1] / dfreq)
            rightfr = round(filt_edge[whichfilt + 2] / dfreq)
            fwidth = (rightfr - leftfr) * dfreq
            height = 2.0 / fwidth

            if centerfr != leftfr:
                leftslope = height / (centerfr - leftfr)
            else:
                leftslope = 0
            freq = leftfr + 1
            while freq < centerfr:
                self.filters[freq, whichfilt] = (freq - leftfr) * leftslope
                freq = freq + 1
            if freq == centerfr:  # This is always true
                self.filters[freq, whichfilt] = height
                freq = freq + 1
            if centerfr != rightfr:
                rightslope = height / (centerfr - rightfr)
            while freq < rightfr:
                self.filters[freq, whichfilt] = (freq - rightfr) * rightslope
                freq = freq + 1
        # Build DCT matrix
        self.s2dct = s2dctmat(nfilt, ncep, 1.0 / nfilt)

    def sig2s2mfc_energy_concat(self, sig, dn=2):
        nfr = int(len(sig) / self.fshift)
        mfcc_concat = numpy.zeros((nfr, (2 * (self.ncep + 1))), "d")
        fr = 0
        while fr < nfr:
            start = int(fr * self.fshift)
            end = min(len(sig), start + self.wlen)
            frame = sig[start:end]
            if len(frame) < self.wlen:
                frame = numpy.resize(frame, self.wlen)
                frame[self.wlen :] = 0
            mfcc_concat[fr, : self.ncep] = self.frame2s2mfc(frame)
            mfcc_concat[fr, self.ncep] = math.log(
                1 + numpy.mean(numpy.power(frame.astype(float), 2))
            )
            fr = fr + 1
        fr = 0
        while fr < nfr:
            start = int(fr * self.fshift)
            end = min(len(sig), start + self.wlen)
            frame = sig[start:end]
            if len(frame) < self.wlen:
                frame = numpy.resize(frame, self.wlen)
                frame[self.wlen :] = 0
            for n in range(1, dn + 1):
                future = fr + n if fr + n < nfr else nfr - 1
                past = fr - n if fr - n >= 0 else 0
                mfcc_concat[fr, self.ncep + 1 : -1] += n * (
                    mfcc_concat[future, : self.ncep] - mfcc_concat[past, : self.ncep]
                )
            mfcc_concat[fr, self.ncep + 1 : -1] /= 2 * dn * (dn + 1) * (2 * dn + 1) / 6
            future = (
                mfcc_concat[fr + 1, self.ncep]
                if fr < nfr - 1
                else mfcc_concat[fr, self.ncep]
            )
            mfcc_concat[fr, -1] = future - mfcc_concat[fr, self.ncep]
            fr = fr + 1
        return mfcc_concat

    def pre_emphasis(self, frame):
        # FIXME: Do this with matrix multiplication
        outfr = numpy.empty(len(frame), "d")
        outfr[0] = frame[0] - self.alpha * self.prior
        for i in range(1, len(frame)):
            outfr[i] = frame[i] - self.alpha * frame[i - 1]
        self.prior = frame[-1]
        return outfr

    def frame2logspec(self, frame):
        frame = self.pre_emphasis(frame) * self.win
        fft = numpy.fft.rfft(frame, self.nfft)
        # Square of absolute value
        power = fft.real * fft.real + fft.imag * fft.imag
        return numpy.log(numpy.dot(power, self.filters).clip(1e-5, numpy.inf))

    def frame2s2mfc(self, frame):
        logspec = self.frame2logspec(frame)
        return numpy.dot(logspec, self.s2dct.T) / self.nfilt


class Beat(object):
    def __init__(self, sr, fps=15) -> None:
        self._sr = sr
        self._fps = fps

    def calc_onset(self, wav):
        # raw_onset = librosa.onset.onset_detect(y=wav, sr=self._sr, units='samples', delta = 0.2)
        raw_onset = librosa.onset.onset_detect(y=wav, sr=self._sr, units="samples")
        onset = self.resample_onset(raw_onset, wav.shape[0])
        return onset.reshape((-1, 1))

    def resample_onset(self, peaks, original_len):
        new_len = round(original_len * self._fps / self._sr)
        resampled = np.zeros(new_len)
        for peak in peaks:
            resampled[round(min(peak * self._fps / self._sr, new_len - 1))] = 1
        return resampled


def load_audio_from_wav(file, frate=90, ncep=13):
    wav, sr = librosa.load(file)
    mfcc_class = MFCC(frate=frate, samprate=sr, wlen=0.025, ncep=ncep)
    beat_class = Beat(sr, frate)
    mfcc = deepcopy(mfcc_class.sig2s2mfc_energy_concat(wav))
    mfcc_der = mfcc[:, ncep + 1 :]
    mfcc = mfcc[:, : ncep + 1]
    beat = deepcopy(beat_class.calc_onset(wav))
    if beat.shape[0] > mfcc.shape[0]:
        beat = beat[: mfcc.shape[0] - beat.shape[0], :]
    elif beat.shape[0] < mfcc.shape[0]:
        mfcc = mfcc[: beat.shape[0] - mfcc.shape[0], :]
        mfcc_der = mfcc_der[: beat.shape[0] - mfcc_der.shape[0], :]
    return Audio(wav, sr, beat, mfcc, mfcc_der)


def load_audio_only(file):
    wav, sr = librosa.load(file)
    byte_audio = wav * 32767
    byte_audio = byte_audio.astype(np.int16)
    return wav, byte_audio, sr


class Audio:
    def __init__(self, audio, sr, beat, mfcc, mfcc_der, name=None, path=None):
        self._audio = audio
        self._sr = sr
        self._beat = beat
        self._mfcc = mfcc
        self._mfcc_der = mfcc_der
        self._name = name
        self._path = path

    def change_mfcc(self, new_mfcc):
        self._mfcc = new_mfcc

    def change_mfcc_der(self, new_mfcc_der):
        self._mfcc_der = new_mfcc_der

    def byte_audio(self):
        byte_audio = self._audio * 32767
        byte_audio = byte_audio.astype(np.int16)
        return byte_audio

    def audio(self):
        return self._audio

    def sr(self):
        return self._sr

    def beat(self):
        return self._beat

    def mfcc(
        self,
    ):
        return self._mfcc

    def mfcc_der(
        self,
    ):
        return self._mfcc_der


class AudioDatabase:
    def __init__(self, dir_path, frate, from_path=True, ncep=13):
        self._dir_path = dir_path
        self._frate = frate
        self._ncep = ncep
        if from_path:
            self.load_db_from_path()
        else:
            self.load_db()

    def num_audio(
        self,
    ):
        return len(self._audio_db)

    def get_audio(self, idx):
        return self._audio_db[idx]

    def get_audio_by_name(self, name):
        for m in self._audio_db:
            if m._name == name:
                return m
        return None

    def save_db(
        self,
    ):
        db_dict = {
            "sr": [],
            "audio": [],
            "mfcc": [],
            "mfcc_der": [],
            "beat": [],
            "name": [],
        }
        for anum in range(self.num_audio()):
            audio = self.get_audio(anum)
            db_dict["sr"].append(audio.sr())
            db_dict["audio"].append(audio.audio())
            db_dict["mfcc"].append(audio.mfcc())
            db_dict["mfcc_der"].append(audio.mfcc_der())
            db_dict["beat"].append(audio.beat())
            db_dict["name"].append(audio._name)

        save_filename = "{}/{}".format(self._dir_path, "audio_db.pickle")
        with open(save_filename, "wb") as fw:
            pickle.dump(db_dict, fw)
        print("Audio db saved")

    def load_db(
        self,
    ):
        start_time = time.time()
        if os.path.exists(self._dir_path):
            self._audio_db = []
            beat_class = None
            print("Loading the Audio DB")
            mfcc_all = np.zeros((0, self._ncep + 1))
            for file_path in tqdm(natsort.natsorted(os.listdir(self._dir_path))):
                if file_path.endswith(".wav"):
                    path = "{}/{}".format(self._dir_path, file_path)
                    wav, sr = librosa.load(path)
                    mfcc_class = MFCC(
                        frate=self._frate, samprate=sr, wlen=0.025, ncep=self._ncep
                    )
                    if beat_class is None:
                        beat_class = Beat(sr, self._frate)
                    beat = deepcopy(beat_class.calc_onset(wav))
                    mfcc = deepcopy(mfcc_class.sig2s2mfc_energy_concat(wav))
                    mfcc_der = mfcc[:, self._ncep + 1 :]
                    mfcc = mfcc[:, : self._ncep + 1]
                    self._audio_db.append(
                        Audio(wav, sr, beat, mfcc, mfcc_der, file_path[:-4], path)
                    )
                    mfcc_all = np.concatenate((mfcc_all, mfcc), axis=0)
                    del mfcc_class
            del beat_class
            self.mfcc_mean, self.mfcc_std = get_data_stats(mfcc_all)
            print("Audio DB load : {} sec".format(time.time() - start_time))
            self.save_db()

    def load_db_from_path(
        self,
    ):
        start_time = time.time()
        print("Loading the Audio DB")
        if os.path.exists(self._dir_path):
            for file_path in natsort.natsorted(os.listdir(self._dir_path)):
                if file_path.endswith(".pickle"):
                    path = "{}/{}".format(self._dir_path, file_path)
                    with open(path, "rb") as fr:
                        db = pickle.load(fr)
                    self._audio_db = []
                    beat_class = None
                    n_db = len(db["audio"])
                    mfcc_all = np.zeros((0, self._ncep + 1))
                    for i in range(n_db):
                        path = self._dir_path + db["name"][i] + ".wav"
                        self._audio_db.append(
                            Audio(
                                db["audio"][i],
                                db["sr"][i],
                                db["beat"][i],
                                db["mfcc"][i],
                                db["mfcc_der"][i],
                                db["name"][i],
                                path,
                            )
                        )
                        mfcc_all = np.concatenate((mfcc_all, db["mfcc"][i]), axis=0)
        self.mfcc_mean, self.mfcc_std = get_data_stats(mfcc_all)
        print("Audio DB load : {} sec".format(time.time() - start_time))


class PlayAudioDatabase:
    def __init__(self, dir_path):
        self._dir_path = dir_path
        self.load_db()

    def load_db(
        self,
    ):
        start_time = time.time()
        if os.path.exists(self._dir_path):
            self._audio_db = []
            for file_path in natsort.natsorted(os.listdir(self._dir_path)):
                if file_path.endswith(".wav"):
                    path = "{}/{}".format(self._dir_path, file_path)
                    audio = load_audio_only(path)
                    self._audio_db.append(audio)
            print("Audio DB load : {} sec".format(time.time() - start_time))

    def get_audio(self, idx):
        return self._audio_db[idx]
