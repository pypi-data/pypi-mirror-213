from vaaibody.viewer.camera import FreeCamera, TargetCamera


class Controller:
    def __init__(self, owner):
        self._param_class = None
        self._owner = owner
        self._name = "Controller"

        self._free_camera = FreeCamera()
        self._target_camera = TargetCamera()
        self._current_camera = self._target_camera
        self._track = True

    @property
    def name(self):
        return self._name

    def draw(self, viewr=None):
        pass

    def tick(self, current_pose=None):
        pass

    def get_parameter(self):
        return []

    def get_parameter_class(self):
        return self._param_class

    def get_free_camera(self):
        self._free_camera.set_look_at_and_eye(
            self._current_camera._look_at, self._current_camera._eye
        )
        self._current_camera = self._free_camera
        return self._free_camera

    def get_target_camera(self):
        self._target_camera.change_look_at(self._current_camera._look_at)
        self._current_camera = self._target_camera
        return self._target_camera

    def toggle_track(self):
        self._track = not self._track
