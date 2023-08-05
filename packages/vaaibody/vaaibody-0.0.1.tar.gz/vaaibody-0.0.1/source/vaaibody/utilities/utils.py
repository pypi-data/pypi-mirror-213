import numpy as np
import math

""""
String, Math utils.
"""


def get_swap_dict(d):
    return {v: k for k, v in d.items()}


def selected_string(str, is_selected):
    if is_selected:
        return "[" + str + "]"
    else:
        return str


# restore rotation matrix from matrix6d
def restore_matrix6d(matrix6d):
    axis_x = matrix6d[0:3]
    axis_z = np.cross(axis_x, matrix6d[3:6])
    axis_y = np.cross(axis_z, axis_x)
    axis_x /= np.linalg.norm(axis_x)
    axis_y /= np.linalg.norm(axis_y)
    axis_z /= np.linalg.norm(axis_z)

    return np.array([axis_x, axis_y, axis_z]).T


def get_data_stats(data):
    data_mean = np.expand_dims(data.mean(axis=0), axis=0)
    data_std = np.expand_dims(data.std(axis=0), axis=0)
    return data_mean, data_std


def normalize_data(data, mean, std):
    # Z-score normalization
    return (data - mean) / (std + 1e-8)


def vec_to_skew(v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])


def rotation_mtx_from_vectors(a, b):
    # First make each vectors to unit vectors.
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)

    # Calculate v, s, c
    v = np.cross(a, b)
    s = np.linalg.norm(v)
    c = np.dot(a, b)
    skew_v = vec_to_skew(v)

    R_ba = np.eye(3) + skew_v + np.dot(skew_v, skew_v) * (1 - c) / (s**2)
    return R_ba


def angle_between_two_vectors(a, b, is_cos=False, is_rad=False):
    cos_thet = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    if is_cos:
        return cos_thet
    else:
        if is_rad:
            return math.acos(cos_thet)
        else:
            return math.acos(cos_thet) * 180 / math.pi
