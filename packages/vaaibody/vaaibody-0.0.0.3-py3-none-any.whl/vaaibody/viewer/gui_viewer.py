import time

import glfw
import imgui
import numpy as np
from core.frame import Frame
from imgui.integrations.glfw import GlfwRenderer
from OpenGL.GL.shaders import *
from OpenGL.GLU import *

from viewer.controller import Controller
from viewer.handler import *
from viewer.item_drawer import *


class MainWindow(
    KeyEventHandler,
    MouseButtonEventHandler,
    ScrollEventHandler,
    CursorPosEventHandler,
    WindowSizeEventHandler,
):
    def __init__(self):
        if not glfw.init():
            exit(0)
            return

        self._name = "Main window"
        self._width, self._height = 1790, 930
        self._window = glfw.create_window(
            self._width, self._height, self._name, None, None
        )
        if not self._window:
            glfw.terminate()
            exit(0)
            return
        glfw.set_window_pos(self._window, 5, 50)

        glfw.make_context_current(self._window)
        glfw.swap_interval(0)

        self._fovy = 90
        self._width, self._height = glfw.get_framebuffer_size(self._window)
        ratio = self._width / float(self._height)
        glViewport(0, 0, self._width, self._height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, ratio, 0.01, 1000)

        imgui.create_context()
        io = imgui.get_io()
        io.display_size = 700, 700
        io.fonts.get_tex_data_as_rgba32()

        self._imgui_renderer = GlfwRenderer(self._window, True)

        glfw.set_key_callback(self._window, self.event_key)
        glfw.set_mouse_button_callback(self._window, self.event_mouse_button)
        glfw.set_scroll_callback(self._window, self.event_scroll)
        glfw.set_cursor_pos_callback(self._window, self.event_cursor_pos)
        glfw.set_window_size_callback(self._window, self.event_window_size)

        file = open("data/shader/shader_vert.txt")
        vertex_shader_src = file.read()
        file.close()
        file = open("data/shader/shader_frag.txt")
        frag_shader_src = file.read()
        file.close()

        self._shader = glCreateProgram()
        vertex_shader = compileShader(vertex_shader_src, GL_VERTEX_SHADER)
        frag_shader = compileShader(frag_shader_src, GL_FRAGMENT_SHADER)

        glAttachShader(self._shader, vertex_shader)
        glAttachShader(self._shader, frag_shader)

        glLinkProgram(self._shader)

        glDeleteShader(vertex_shader)
        glDeleteShader(frag_shader)

        self._main_controller = Controller(self)

        self._right_press = False
        self._left_press = True
        self.play_motion = True
        self._current_frame = 0
        self._current_motion_idx = 0
        self._selected_module = None
        self._cursor_pressed = False
        self._init_camera = True
        self._mouse_x = 0
        self._mouse_y = 0
        self._viewer_mode = "recorded"

    def set_skeleton(self, skeleton):
        self._skeleton = skeleton
        self._time_step = self._skeleton._frame_time

    def set_db(self, db):
        self._db = db
        self._current_db_path = self._db.dir_path
        self._drawer_list = {
            Frame: FrameDrawer(),
            Point: PointDrawer(),
            PointWithDirection: PointWithDirectionDrawer(),
        }
        self.set_item_list(
            [Item(self._db.get_motion(self._current_motion_idx), [0])], None
        )
        self.set_mode("recorded")

    def set_motion(self, motion, color=3):
        self._drawer_list = {
            Frame: FrameDrawer(),
            Point: PointDrawer(),
            PointWithDirection: PointWithDirectionDrawer(),
        }
        self.set_item_list([Item(motion, [color])])
        self.set_mode("recorded")

    @property
    def play_motion(self):
        return self._play_motion

    @play_motion.setter
    def play_motion(self, value):
        self._play_motion = value
        self.start_play()

    def start_play(self):
        if self._play_motion:
            self._last_tick_time = time.time()

    def set_item_list(self, item_list, current_module=None):
        self._item_list = item_list
        self._current_frame = 0
        self._num_of_frame = 0
        self.update_item_list()
        self.start_play()

    def update_item_list(self):
        for item in self._item_list:
            n_frame = item.num_frame()
            if (n_frame is not None) and (n_frame > self._num_of_frame):
                self._num_of_frame = n_frame

    def set_mode(self, new_mode):
        if new_mode == "interactive":
            self.set_interactive_mode()
        elif new_mode == "recorded":
            self.set_recorded_mode()
        else:
            print("Error : undefined viewer mode!")

    def set_interactive_mode(self):
        if self._viewer_mode == "interactive":
            return
        self._viewer_mode = "interactive"
        self._current_frame = self._num_of_frame - 1
        self.play_motion = True

    def set_recorded_mode(self):
        if self._viewer_mode == "recorded":
            return
        self._viewer_mode = "recorded"

    def relay_event(self, ClassType, event_function, *args, **kwargs):
        if self._selected_module is not None:
            if isinstance(self._selected_module, ClassType):
                getattr(self._selected_module, event_function)(*args, **kwargs)
            if isinstance(self._selected_module._selected_controller, ClassType):
                getattr(self._selected_module._selected_controller, event_function)(
                    *args, **kwargs
                )

    def event_window_size(self, window, new_width, new_height):
        self._imgui_renderer.resize_callback(window, new_width, new_height)

        self._width, self._height = new_width, new_height
        glViewport(0, 0, self._width, self._height)

        self.display()

        self.relay_event(
            WindowSizeEventHandler, "event_window_size", window, new_width, new_height
        )

    def event_mouse_button(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                self._left_press = True
            elif action == glfw.RELEASE:
                self._left_press = False

        elif button == glfw.MOUSE_BUTTON_RIGHT:
            if action == glfw.PRESS:
                self._right_press = True

            elif action == glfw.RELEASE:
                self._right_press = False

        self.relay_event(
            MouseButtonEventHandler, "event_mouse_button", window, button, action, mods
        )

    def event_cursor_pos(self, window, x, y):
        if self._right_press:
            self._camera.rotate(
                x, y, self._mouse_x, self._mouse_y, min(self._width, self._height) / 2.0
            )

        if not self.get_current_controller()._track:
            if self._left_press:
                self._camera = self.get_current_controller().get_free_camera()
                self._camera.translation_xy(x, y, self._mouse_x, self._mouse_y)

        self._mouse_x = x
        self._mouse_y = y

        self.relay_event(CursorPosEventHandler, "event_cursor_pos", window, x, y)

    def event_scroll(self, window, x_offset, y_offset):
        self._imgui_renderer.scroll_callback(window, x_offset, y_offset)
        if not imgui.is_window_hovered(imgui.HOVERED_ANY_WINDOW):
            if glfw.get_key(self._window, glfw.KEY_LEFT_SHIFT):
                if y_offset > 0:
                    self.set_mode("recorded")
                    self.play_motion = False
                    self.prev()
                elif y_offset < 0:
                    self.next()
            elif hasattr(self, "_camera"):
                self._camera.dolly(y_offset)

        self.relay_event(ScrollEventHandler, "event_scroll", window, x_offset, y_offset)

    def event_key(self, window, key, scancode, action, mods):
        self._imgui_renderer.keyboard_callback(window, key, scancode, action, mods)
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:  # exit
                glfw.set_window_should_close(window, GL_TRUE)

            elif key == glfw.KEY_T:
                self.get_current_controller().toggle_track()

            if key == glfw.KEY_SPACE:
                self.play_motion = not self.play_motion

        if key == glfw.KEY_G:
            if action == glfw.PRESS:
                self._cursor_pressed = True
            if action == glfw.RELEASE:
                self._cursor_pressed = False

        self.custom_keys(window, key, scancode, action, mods)

        self.relay_event(
            KeyEventHandler, "event_key", window, key, scancode, action, mods
        )

    def custom_keys(self, window, key, scancode, action, mods):
        pass

    def get_camera_front_vector2d(self):
        near, far = self.mouse_to_ray(self._width / 2, self._height / 2)
        diff = far - near
        diff[1] = 0.0
        diff /= np.linalg.norm(diff)
        return diff

    def mouse_to_ray(self, x, y, local_transform=False):
        x = float(x)
        y = self._height - float(y)
        pmat = (GLdouble * 16)()
        mvmat = (GLdouble * 16)()
        viewport = (GLint * 4)()
        px = (GLdouble)()
        py = (GLdouble)()
        pz = (GLdouble)()
        glGetIntegerv(GL_VIEWPORT, viewport)
        glGetDoublev(GL_PROJECTION_MATRIX, pmat)
        mvmat = (GLdouble * 16)()
        glGetDoublev(GL_MODELVIEW_MATRIX, mvmat)
        px, py, pz = gluUnProject(x, y, 1, mvmat, pmat, viewport)
        ray_far = np.array([px, py, pz])
        px, py, pz = gluUnProject(x, y, 0, mvmat, pmat, viewport)
        ray_near = np.array([px, py, pz])
        return ray_near, ray_far

    def draw(self, data_object, color, is_shadow=False):
        if type(data_object) is list:
            for idx, d in enumerate(data_object):
                c_idx = idx % len(color)
                self.draw(d, [color[c_idx]], is_shadow)
        else:
            self._drawer_list[type(data_object)].draw(data_object, color[0], is_shadow)

    def get_drawer(self, item):
        if type(item) in self._drawer_list.keys():
            return self._drawer_list[type(item)]
        else:
            return self.get_drawer(item[0])

    def get_current_controller(self):
        if self._selected_module is None:
            current_controller = self._main_controller
        else:
            current_controller = self._selected_module._selected_controller
        return current_controller

    def display(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        for item in self._item_list:
            drawer = self.get_drawer(item.data_object)
            center = drawer.center(item.data_object[self._current_frame])
            if center is not None:
                break

        current_controller = self.get_current_controller()
        if current_controller._track:
            self._camera = current_controller.get_target_camera()
            self._camera.change_look_at(center)
            if self._init_camera:
                self._camera.rotate_direction(90, 0, 0)
                self._init_camera = False
        else:
            self._camera = current_controller.get_free_camera()

        self._camera.apply(self._window)

        glUseProgram(self._shader)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # mirror
        glPushMatrix()
        glScalef(1.0, -1.0, 1.0)
        ru.init_lights(center)
        for item in self._item_list:
            if item.data_object is None or len(item.data_object) == 0:
                continue
            self.draw(
                item.data_object[min(self._current_frame, len(item.data_object) - 1)],
                item.color,
                is_shadow=True,
            )
        glPopMatrix()

        ru.init_lights(center)
        ru.draw_ground(center)
        for item in self._item_list:
            if item.data_object is None or len(item.data_object) == 0:
                continue
            self.draw(
                item.data_object[min(self._current_frame, len(item.data_object) - 1)],
                item.color,
            )
        self.custom_display()

    # For custom purpose
    def custom_display():
        pass

    def spin_lock(self, sleep_time):
        start_time = time.time()
        while time.time() - start_time < sleep_time:
            pass

    def prev(self):
        if self._current_frame > 0:
            self._current_frame -= 1
        else:
            self._current_frame = 0
            self.play_motion = False

    def next(self):
        if self._current_frame < self._num_of_frame - 1:
            self._current_frame += 1
        else:
            self._current_frame = self._num_of_frame - 1
            self.play_motion = False

    def event_handling(self):
        glfw.poll_events()

        self._imgui_renderer.process_inputs()

        self.relay_event(UserInputHandler, "update_user_input", self._window)

    def async_tick(self):
        self.relay_event(AsyncTickHandler, "async_tick")

    def sync_tick(self):
        if self.play_motion:
            elapsed_time = time.time() - self._last_tick_time
            for _ in range(round(elapsed_time / self._time_step)):
                self.next()
                self._last_tick_time += self._time_step

    def rendering(self):
        self.display()
        self._imgui_renderer.render(imgui.get_draw_data())
        glfw.swap_buffers(self._window)

    def loop(self):
        self._current_frame = 0
        while not glfw.window_should_close(self._window):
            # event handling
            self.event_handling()

            # async tick
            self.async_tick()

            # tick
            self.sync_tick()

            # rendering
            self.rendering()
        glfw.terminate()
