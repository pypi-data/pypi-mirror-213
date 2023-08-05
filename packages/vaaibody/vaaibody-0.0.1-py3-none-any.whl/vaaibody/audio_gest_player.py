import imgui
import simpleaudio as sa

from vaaibody.core.audio import PlayAudioDatabase
from vaaibody.core.modAudio import *
from vaaibody.core.motion import MotionDatabase
from vaaibody.core.skeleton import Skeleton
from vaaibody.viewer.gui_viewer import MainWindow
from vaaibody.viewer.item_drawer import *


class MyWindow(MainWindow):
    def __init__(self, skeleton, db, audio_db):
        super().__init__()
        self.set_skeleton(skeleton)
        self.set_db(db)
        self.audio_db = audio_db
        test_audio = self.audio_db.get_audio(0)
        self._byte_audio = test_audio[1]
        self._sr = test_audio[2]
        self.gen_audio()

    # Overriding
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
            self.stop_audio()

    def gen_audio(
        self,
    ):
        aud_frame = min(
            int(self._current_frame * self._sr * self._time_step),
            len(self._byte_audio) - 1,
        )
        self.mod_obj = myPlayObject(
            sa.play_buffer(self._byte_audio[aud_frame:], 1, 2, self._sr).play_id
        )

    def stop_audio(
        self,
    ):
        sa.stop_all()
        del self.mod_obj
        self.mod_obj = None

    def change_audio(
        self,
    ):
        self.stop_audio()
        test_audio = self.audio_db.get_audio(self._current_motion_idx)
        self._byte_audio = test_audio[1]
        self._sr = test_audio[2]
        self.gen_audio()

    def custom_display(self):
        imgui.new_frame()
        imgui.begin("custom window", True)
        if imgui.button("prev"):
            self._current_motion_idx -= 1
            if self._current_motion_idx < 0:
                self._current_motion_idx = self._db.num_motion() - 1
            self.set_item_list(
                [Item([self._db.get_motion(self._current_motion_idx)], "prev")]
            )
            self.change_audio()
        imgui.same_line()
        if imgui.button("next"):
            self._current_motion_idx += 1
            if self._current_motion_idx >= self._db.num_motion():
                self._current_motion_idx = 0
            self.set_item_list(
                [Item([self._db.get_motion(self._current_motion_idx)], "next")]
            )
            self.change_audio()
        # motion selector
        imgui.listbox_header("Motion list", height=200)
        for i in range(self._db.num_motion()):
            clicked, _ = imgui.selectable(
                self._db.get_motion(i).file_path.split("/")[-1],
                self._current_motion_idx == i,
                imgui.SELECTABLE_ALLOW_DOUBLE_CLICK,
            )
            if clicked:
                self._current_motion_idx = i
                self.set_item_list(
                    [Item(self._db.get_motion(self._current_motion_idx), [0])]
                )
                self.change_audio()
                self.set_mode("recorded")
        imgui.listbox_footer()
        if imgui.button("prev"):
            self._current_motion_idx -= 1
            if self._current_motion_idx < 0:
                self._current_motion_idx = self._db.num_motion() - 1
            self.set_item_list(
                [Item(self._db.get_motion(self._current_motion_idx), [0])]
            )
            self.set_mode("recorded")
        imgui.same_line()
        if imgui.button("next"):
            self._current_motion_idx += 1
            if self._current_motion_idx >= self._db.num_motion():
                self._current_motion_idx = 0
            self.set_item_list(
                [Item(self._db.get_motion(self._current_motion_idx), [0])]
            )
            self.set_mode("recorded")
        imgui.spacing()
        if self._selected_module is not None:
            self._selected_module.draw_imgui(self)
        imgui.end()
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
        imgui.render()
        imgui.end_frame()

        self._imgui_renderer.render(imgui.get_draw_data())


if __name__ == "__main__":
    skeleton = Skeleton(name="Gesture_Before")
    skeleton.load_hierarchy_from_bvh("data/motion/Gesture_Before/VAAI_Basic_01_01.bvh")
    db = MotionDatabase(skeleton, "data/motion/Gesture_Before/")
    audio_db = PlayAudioDatabase("data/audio/Gesture_Audio_Fin")
    main_window = MyWindow(skeleton, db, audio_db)
    main_window.loop()
