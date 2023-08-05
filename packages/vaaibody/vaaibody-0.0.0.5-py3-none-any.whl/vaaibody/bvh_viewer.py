import os

import glfw
import imgui

from vaaibody.core.motion import MotionDatabase
from vaaibody.core.skeleton import Skeleton
import natsort
from vaaibody.viewer.gui_viewer import MainWindow
from vaaibody.viewer.item_drawer import *


class MyWindow(MainWindow):
    def __init__(self, skeleton, db):
        super().__init__()
        self.set_skeleton(skeleton)
        self.set_db(db)
        self.selected = 0

    # 여기에 custom key binding 코드 작성
    def custom_keys(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            if key == glfw.KEY_COMMA:
                skel_dict = self._skeleton.joint_dict.keys()
                # self.texts.remove(list(skel_dict)[self.selected])
                self.selected = (
                    self.selected + 1 if self.selected < len(list(skel_dict)) - 1 else 0
                )
                # self.texts.append(list(skel_dict)[self.selected])

            if key == glfw.KEY_PERIOD:
                skel_dict = self._skeleton.joint_dict.keys()
                # self.texts.remove(list(skel_dict)[self.selected])
                self.selected = (
                    self.selected - 1 if self.selected > 0 else len(list(skel_dict)) - 1
                )
                # self.texts.append(list(skel_dict)[self.selected])

            if key == glfw.KEY_A:
                pass
                # current_motion = self._db.get_motion(self._current_motion_idx)
                # new_motion = mirror_motion(current_motion)
                # self._db.append_motion(new_motion)

    # 여기에 custom display 코드 작성
    def custom_display(
        self,
    ):
        imgui.new_frame()
        imgui.begin("custom window", True)
        if imgui.button("prev"):
            self._current_motion_idx -= 1
            if self._current_motion_idx < 0:
                self._current_motion_idx = self._db.num_motion() - 1
            self.set_item_list(
                [Item([self._db.get_motion(self._current_motion_idx)], "prev")]
            )
        imgui.same_line()
        if imgui.button("next"):
            self._current_motion_idx += 1
            if self._current_motion_idx >= self._db.num_motion():
                self._current_motion_idx = 0
            self.set_item_list(
                [Item([self._db.get_motion(self._current_motion_idx)], "next")]
            )

        # db selector
        imgui.text("Current DB : {}".format(self._db.dir_path))
        imgui.listbox_header("DB list", height=50)
        db_lists = os.listdir("data/motion/")
        db_lists.sort()
        for db_path in db_lists:
            clicked, _ = imgui.selectable(
                db_path,
                self._current_db_path == db_path,
                imgui.SELECTABLE_ALLOW_DOUBLE_CLICK,
            )
            if clicked:
                if self._current_db_path != db_path:
                    self._current_db_path = db_path
                    for file_path in natsort.natsorted(
                        os.listdir("data/motion/" + db_path)
                    ):
                        if file_path.endswith(".bvh"):
                            self._skeleton = Skeleton("Skel_" + db_path)
                            self._skeleton.load_hierarchy_from_bvh(
                                "data/motion/" + db_path + "/" + file_path
                            )
                            self._time_step = self._skeleton._frame_time
                            self._db = MotionDatabase(
                                self._skeleton, "data/motion/" + db_path
                            )
                            self.selected = 0
                            break
        imgui.listbox_footer()

        # motion selector
        imgui.listbox_header("Motion list", height=200)

        for i in range(self._db.num_motion()):
            clicked, _ = imgui.selectable(
                self._db.get_motion(i).file_path.split("/")[-1],
                self._current_motion_idx == i,
                imgui.SELECTABLE_ALLOW_DOUBLE_CLICK,
            )
            if clicked:
                self._play_motion = False
                self._current_motion_idx = i
                self.set_item_list(
                    [Item(self._db.get_motion(self._current_motion_idx), [0])]
                )
                # self.set_item_list([Item(self._db.get_motion(self._current_motion_idx), [3]),Item(self.new_db.get_motion(self._current_motion_idx), [0])], None)
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
        self.draw_selected()

    def draw_selected(
        self,
    ):
        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(
            *self._item_list[0][self._current_frame].get_global_translation(
                self.selected
            )
        )
        ru.draw_sphere(0.01)
        glPopMatrix()


if __name__ == "__main__":
    skeleton = Skeleton(name="AudioGest")
    skeleton.load_hierarchy_from_bvh("data/motion/AudioGest/s14_take11_shallow.bvh")
    db = MotionDatabase(skeleton, "data/motion/AudioGest/")

    main_window = MyWindow(skeleton, db)
    main_window.loop()
