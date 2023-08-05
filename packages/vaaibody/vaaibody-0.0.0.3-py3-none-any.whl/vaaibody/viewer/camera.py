import numpy as np
import math
import glfw

from OpenGL.GL import *
from OpenGL.GLU import *
from scipy.spatial.transform import Rotation as R


class TargetCamera:
    def __init__(self):
        self._fovy = 45.0
        self._look_at = np.array([0.0, 0.8, 0.0])
        self._eye = np.array([3.0, 1.5, 0.0])
        self._up_vector = np.array([0.0, 1.0, 0.0])

    def clip_z(self):
        # prevent camera from penetrating ground
        self._eye[1] = max(self._eye[1], 0.1)

    def rotate(self, x, y, prev_x, prev_y, r):
        angle_x = math.atan2(y - prev_y, r)
        angle_y = math.atan2(x - prev_x, r)

        n = self._look_at - self._eye
        axis_x = np.cross(np.array([0.0, 1.0, 0.0]), n)
        axis_x /= np.linalg.norm(axis_x)

        n = R.from_rotvec(-angle_y * np.array([0.0, 1.0, 0.0])).apply(n)
        n = R.from_rotvec(angle_x * axis_x).apply(n)

        self._eye = self._look_at - n
        self.clip_z()

    def rotate_direction(self, dir_x, dir_y, r):
        x, y = self._eye[0] + dir_x, self._eye[2] + dir_y
        self.rotate(x, y, self._eye[0], self._eye[2], r)

    def dolly(self, direction):
        delta = self._eye - self._look_at
        scale = np.linalg.norm(delta)
        new_scale = max(1.0, scale - direction * 0.2)
        delta *= new_scale / scale
        self._eye = self._look_at + delta
        self.clip_z()

    def change_look_at(self, new_look_at):
        delta = self._eye - self._look_at
        self._look_at = new_look_at
        self._eye = self._look_at + delta
        self.clip_z()

    def set_look_at_and_eye(self, new_look_at, new_eye):
        self._look_at = new_look_at
        self._eye = new_eye
        self.clip_z()

    def apply(self, window):
        self._window = window
        width, height = glfw.get_framebuffer_size(self._window)
        if height <= 0:
            return
        ratio = width / float(height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self._fovy, ratio, 0.01, 1000)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(*self._eye, *self._look_at, *self._up_vector)

    def get_front_vector(self):
        direction = self._look_at - self._eye
        direction[1] = 0
        dist = np.linalg.norm(direction)
        if dist > 0:
            direction /= dist
        return direction


class FreeCamera(TargetCamera):
    def __init__(self):
        self._fovy = 45.0
        self._look_at = np.array([0.0, 0.8, 0.0])
        self._eye = np.array([3.0, 1.5, 0.0])
        self._up_vector = np.array([0.0, 1.0, 0.0])

    def translation_xy(self, x, y, prev_x, prev_y):
        delta_x, delta_y = 0.001 * (prev_x - x), 0.001 * (prev_y - y)

        axis_y = self._look_at - self._eye
        axis_x = np.cross(np.array([0.0, 1.0, 0.0]), axis_y)
        axis_x /= np.linalg.norm(axis_x)

        prev_look_z, prev_eye_z = self._look_at[1], self._eye[1]
        delta = delta_x * axis_x + delta_y * axis_y
        self._look_at += delta
        self._eye += delta
        self._look_at[1] = prev_look_z
        self._eye[1] = prev_eye_z

    def translation_xy_direction(self, dir_x, dir_y):
        x, y = self._eye[0] + dir_x, self._eye[2] + dir_y
        self.translation_xy(x, y, self._eye[0], self._eye[2])
