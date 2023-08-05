from typing import List, Tuple
from core.audio import Audio
import numpy as np


def cut_audio(original_audio: Audio, st_time=0, end_time=-1):
    if end_time == -1:
        end_frm = original_audio.audio().shape[0]
    else:
        end_frm = min(original_audio.audio().shape[0], original_audio.sr() * end_time)
    st_frm = max(0, st_time * original_audio.sr())

    # return new_audio


def silent_detector(
    mfcc_feature: np.ndarray,
    std_thresh: int = 0,
    duration: int = 60,
    std_log_energy_idx: int = 13,
) -> Tuple[List, np.ndarray]:
    """
    Args
        mfcc_feature
    Returns
        silence_inx: list
        silencer: np.ndarray

    """
    n_features = len(mfcc_feature)
    silencer = np.zeros(n_features)
    silence_idx = []
    cont_silence_cnt = 0
    for i in range(n_features):
        if mfcc_feature[i][std_log_energy_idx] < std_thresh:
            cont_silence_cnt += 1
            if cont_silence_cnt == duration:
                for sub in range(duration):
                    silence_idx.append(i - sub)
                    silencer[i - sub] = 1
            elif cont_silence_cnt > duration:
                silence_idx.append(i)
                silencer[i] = 1
        else:
            cont_silence_cnt = 0
    silence_idx.sort()
    return silence_idx, silencer
