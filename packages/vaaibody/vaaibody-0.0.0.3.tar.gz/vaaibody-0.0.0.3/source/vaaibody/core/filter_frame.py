from utilities.filter import *
from utilities.frame_utils import *

"""
TO DO
Make it compatable for action
"""


class actionFilterDefault(object):
    def __init__(self, init_action: np.ndarray, sampling_rate=60, num_joints=186):
        self.init_action = init_action
        self.sampling_rate = sampling_rate
        self.num_joints = num_joints
        self.highcut = [5.0]
        self._action_filter = self._BuildActionFilter()
        self.prev_action = init_action[-1]
        self._ResetActionFilter()

    def _BuildActionFilter(self):
        a_filter = ActionFilterButter(
            sampling_rate=self.sampling_rate,
            highcut=self.highcut,
            num_joints=self.num_joints,
        )
        return a_filter

    def _ResetActionFilter(self):
        self._action_filter.reset()
        # self._action_filter.init_history_with_motion(self.init_action)
        self._action_filter.init_history(self.init_action[-1])

    def _FilterAction(self, action):
        action = make_cont_frame(self.prev_action, action)
        filtered_action = self._action_filter.filter(action)
        self.prev_action = filtered_action.copy()
        filtered_action = make_range_frame(filtered_action)
        return filtered_action
