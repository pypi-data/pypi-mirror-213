import time

import glfw
import imgui
import numpy as np
import simpleaudio as sa
from vaaibody.core.modAudio import *
from scipy.spatial.transform import Rotation as R
from vaaibody.utilities.frame_utils import *

from vaaibody.viewer.gui_viewer import MainWindow
from vaaibody.viewer.item_drawer import *


class GestureWindow(MainWindow):
    def __init__(self, skel, searched_motion, test_audio, sil_hint):
        super().__init__()
        self.set_skeleton(skel)
        self.set_motion(searched_motion)
        self._searched_motion = searched_motion
        self.sil_hint = sil_hint
        self.graph_tm = 60
        self._audio_module = test_audio
        self._byte_audio = self._audio_module.byte_audio()
        self._sr = self._audio_module.sr()
        self.play_motion = False
        self.mod_obj = None
        self.mo_vel = get_position_vel(searched_motion).transpose()
        self.mo_vel = np.pad(
            self.mo_vel, ((0, 0), (self.graph_tm, 0)), "constant", constant_values=0
        )

    def calc_tranforms_for_rendering(self, searched_motion):
        skel = searched_motion.skeleton
        global_transforms_trans = [None for _ in range(skel.num_joints())]
        global_transforms_rot = [None for _ in range(skel.num_joints())]
        component_transforms_trans = [None for _ in range(skel.num_joints())]
        component_transforms_rot = [None for _ in range(skel.num_joints())]
        local_transforms_trans = [None for _ in range(skel.num_joints())]
        local_transforms_rot = [None for _ in range(skel.num_joints())]
        root_transforms_inv_trans = [
            x._root_transform_inv.translation for x in searched_motion._frames
        ]
        root_transforms_inv_rot = [
            x._root_transform_inv.rotation_np for x in searched_motion._frames
        ]
        for idx_joint in range(len(skel.joints)):
            local_transforms_trans[idx_joint] = [
                x._local_transforms[idx_joint].translation
                for x in searched_motion._frames
            ]
            local_transforms_rot[idx_joint] = [
                x._local_transforms[idx_joint].rotation_np
                for x in searched_motion._frames
            ]
            local_transforms_rot[idx_joint] = R.from_matrix(
                np.array(local_transforms_rot[idx_joint])
            )

        local_transforms_trans = np.array(local_transforms_trans)
        root_transforms_inv_trans = np.array(root_transforms_inv_trans)
        root_transforms_inv_rot = R.from_matrix(np.array(root_transforms_inv_rot))

        for idx_joint, joint in enumerate(skel.joints):
            if idx_joint == 0:
                global_transforms_trans[idx_joint] = local_transforms_trans[idx_joint]
                global_transforms_rot[idx_joint] = local_transforms_rot[idx_joint]
            else:
                global_transforms_rot[idx_joint] = (
                    global_transforms_rot[skel.joint_dict[joint.parent.name]]
                    * local_transforms_rot[idx_joint]
                )
                global_transforms_trans[idx_joint] = global_transforms_trans[
                    skel.joint_dict[joint.parent.name]
                ]
                +global_transforms_rot[skel.joint_dict[joint.parent.name]].apply(
                    local_transforms_trans[idx_joint]
                )

            component_transforms_rot[idx_joint] = (
                root_transforms_inv_rot * global_transforms_rot[idx_joint]
            )
            component_transforms_trans[
                idx_joint
            ] = root_transforms_inv_trans + root_transforms_inv_rot.apply(
                global_transforms_trans[idx_joint]
            )

        return np.swapaxes(np.array(global_transforms_trans), 0, 1), np.swapaxes(
            np.array(component_transforms_trans), 0, 1
        )

    # Override methods
    def display(self):
        super().display()
        self.custom_display()

    def sync_tick(self):
        if self.play_motion:
            if self.mod_obj == None:
                self.gen_audio()
            elapsed_time = time.time() - self._last_tick_time
            for _ in range(round(elapsed_time / self._time_step)):
                self.next()
                self.mod_obj.wait_done(frame_time=0.00000001)
                self._last_tick_time += self._time_step
        else:
            sa.stop_all()
            if self.mod_obj is not None:
                del self.mod_obj
            self.mod_obj = None

    # Customize methods
    def gen_audio(
        self,
    ):
        aud_frame = int(self._current_frame * self._sr * self._time_step)
        self.mod_obj = myPlayObject(
            sa.play_buffer(self._byte_audio[aud_frame:], 1, 2, self._sr).play_id
        )

    def stop_audio(
        self,
    ):
        sa.stop_all()
        del self.mod_obj
        self.mod_obj = None

    def plot_joint_vel(self, joint_name):
        if self._skeleton.joint_dict.get(joint_name) is None:
            print("There is no joint named ", joint_name)
            return
        imgui.plot_lines(
            joint_name + " x",
            100
            * self.mo_vel[
                self._skeleton.joint_dict[joint_name] * 3,
                self._current_frame : self._current_frame + self.graph_tm,
            ],
            overlay_text=joint_name + "_x",
            values_offset=0,
            graph_size=(0, 100),
            scale_min=-200,
            scale_max=200,
        )
        imgui.plot_lines(
            joint_name + " y",
            100
            * self.mo_vel[
                self._skeleton.joint_dict[joint_name] * 3 + 1,
                self._current_frame : self._current_frame + self.graph_tm,
            ],
            overlay_text=joint_name + "_y",
            values_offset=0,
            graph_size=(0, 100),
            scale_min=-200,
            scale_max=200,
        )
        imgui.plot_lines(
            joint_name + " z",
            100
            * self.mo_vel[
                self._skeleton.joint_dict[joint_name] * 3 + 2,
                self._current_frame : self._current_frame + self.graph_tm,
            ],
            overlay_text=joint_name + "_z",
            values_offset=0,
            graph_size=(0, 100),
            scale_min=-200,
            scale_max=200,
        )

    # 여기에 custom key binding 코드 작성
    def custom_keys(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            if key == glfw.KEY_A:
                print("A")

    def custom_display(
        self,
    ):
        imgui.new_frame()
        imgui.set_next_window_size(1300, 60)
        imgui.set_next_window_position(30, 840)
        imgui.begin("", False)
        imgui.push_item_width(1)
        imgui.push_item_width(1150)
        changed, self._current_frame = imgui.slider_int(
            "##slider",
            self._current_frame,
            0,
            self._num_of_frame - 1,
            "%d / " + str(self._num_of_frame - 1),
        )
        if changed and (self._current_frame != self._num_of_frame - 1):
            self.stop_audio()
            self.gen_audio()
            self.set_mode("recorded")
        imgui.same_line()
        if imgui.button("prev"):
            self.set_mode("recorded")
            self.play_motion = False
            self.prev()
        imgui.same_line()
        if imgui.button("stop" if (self.play_motion) else "play"):
            self.play_motion = not self.play_motion
        imgui.same_line()
        if imgui.button("next"):
            self.next()
        imgui.end()

        imgui.begin("Joint velocity", True)
        self.plot_joint_vel("LeftHand")
        self.plot_joint_vel("RightHand")
        imgui.end()

        imgui.begin("Speak / Silent")
        if self.sil_hint[self._current_frame] == 1:
            imgui.text("Silent")
        else:
            imgui.text("Speak")
        imgui.end()
        imgui.render()
        imgui.end_frame()
        self._imgui_renderer.render(imgui.get_draw_data())
