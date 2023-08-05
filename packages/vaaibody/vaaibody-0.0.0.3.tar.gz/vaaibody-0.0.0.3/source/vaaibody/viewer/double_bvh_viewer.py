import imgui, glfw
from core.skeleton import *
from core.frame import Frame
from core.database import MotionDatabase
import natsort
from viewer.gui_viewer import MainWindow
from viewer.item_drawer import *


class DoubleViewer(MainWindow):
    def __init__(
        self,
        skeleton_main: Skeleton,
        db_main: MotionDatabase,
        db_trans: MotionDatabase,
        alpha=0.5,
    ):
        """
        db_main: 원본 db
        db_trans: 투명하게 위에서 볼 db
        alpha: 투명도
        """
        super().__init__()
        self._alpha = alpha
        self._current_trans_motion_idx = 0
        self.set_skeleton(skeleton_main)
        self.set_double_db(db_main, db_trans)

    def set_double_db(self, db_main, db_trans):
        self._db_main = db_main
        self._db_trans = db_trans
        self._drawer_list = {
            Frame: FrameDrawer(),
            Point: PointDrawer(),
            PointWithDirection: PointWithDirectionDrawer(),
        }
        self.set_item_list(
            [
                Item(self._db_main.get_motion(self._current_motion_idx), [3]),
                Item(
                    self._db_trans.get_motion(self._current_trans_motion_idx),
                    [2],
                    self._alpha,
                ),
            ],
            None,
        )

        self.set_mode("recorded")

    # 여기에 custom display 코드 작성
    def custom_display(
        self,
    ):
        imgui.new_frame()
        imgui.begin("custom window", True)
        if imgui.button("prev"):
            self._current_motion_idx -= 1
            if self._current_motion_idx < 0:
                self._current_motion_idx = self._db_main.num_motion() - 1
            self.set_item_list(
                [
                    Item(self._db_main.get_motion(self._current_motion_idx), [3]),
                    Item(
                        self._db_trans.get_motion(self._current_trans_motion_idx),
                        [2],
                        self._alpha,
                    ),
                ],
                "prev",
            )

        imgui.same_line()
        if imgui.button("next"):
            self._current_motion_idx += 1
            if self._current_motion_idx >= self._db_main.num_motion():
                self._current_motion_idx = 0
            self.set_item_list(
                [
                    Item(self._db_main.get_motion(self._current_motion_idx), [3]),
                    Item(
                        self._db_trans.get_motion(self._current_trans_motion_idx),
                        [2],
                        self._alpha,
                    ),
                ],
                "next",
            )

        # motion selector
        imgui.listbox_header("Original Motion list", height=200)
        for i in range(self._db_main.num_motion()):
            clicked, _ = imgui.selectable(
                self._db_main.get_motion(i).file_path.split("/")[-1],
                self._current_motion_idx == i,
                imgui.SELECTABLE_ALLOW_DOUBLE_CLICK,
            )
            if clicked:
                self._play_motion = False
                self._current_motion_idx = i
                self.set_item_list(
                    [
                        Item(self._db_main.get_motion(self._current_motion_idx), [3]),
                        Item(
                            self._db_trans.get_motion(self._current_trans_motion_idx),
                            [2],
                            self._alpha,
                        ),
                    ]
                )
        imgui.listbox_footer()

        imgui.listbox_header("Transparent Motion list", height=200)
        for i in range(self._db_trans.num_motion()):
            clicked, _ = imgui.selectable(
                self._db_trans.get_motion(i).file_path.split("/")[-1],
                self._current_trans_motion_idx == i,
                imgui.SELECTABLE_ALLOW_DOUBLE_CLICK,
            )
            if clicked:
                self._play_motion = False
                self._current_trans_motion_idx = i
                self.set_item_list(
                    [
                        Item(self._db_main.get_motion(self._current_motion_idx), [3]),
                        Item(
                            self._db_trans.get_motion(self._current_trans_motion_idx),
                            [2],
                            self._alpha,
                        ),
                    ]
                )
        imgui.listbox_footer()

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
