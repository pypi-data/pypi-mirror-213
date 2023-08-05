from collections import deque
import pandas as pd
import random


class IdleModule(object):
    def __init__(self, db, idle_file) -> None:
        """
        Idle motion을 초기화
        Current 와 Next를 만들어야 하기 때문에 두 번 만든다.
        """
        self.idle_info = pd.read_csv(idle_file)
        self.idx_list_idle = []
        self.idx_used_idle = deque()
        self.idx_list_manip = []
        self.idx_used_manip = deque()
        self.motion_dict_idle = {}
        self.motion_dict_manip = {}
        self.hold_manip = {}
        self.idle_dict = {}
        self.n_idle_played = 0
        for file_name in self.idle_info["File"]:
            current_info = self.idle_info.loc[self.idle_info["File"] == file_name]
            tag = current_info["Tag"].iloc[0]
            if tag == "idle":
                idx_idle, motion_idle = db.get_idx_motion_by_name(file_name)
                idx_st = int(current_info["Start"].iloc[0])
                idx_end = int(current_info["End"].iloc[0])
                idx_end = None if idx_end == -1 else idx_end
                motion_idle.cut_frame(idx_st, idx_end)
                self.idx_list_idle.append(idx_idle)
                self.motion_dict_idle[idx_idle] = motion_idle
                self.idle_dict[idx_idle] = file_name
                trans_diff = (
                    motion_idle[-1].get_root_transform().translation
                    - motion_idle[0].get_root_transform().translation
                )
                # print(idx_idle, trans_diff)
            elif tag == "manipulator":
                idx_manip, motion_manip = db.get_idx_motion_by_name(file_name)
                # mirror_motion(motion_manip)
                idx_st = int(current_info["Start"].iloc[0])
                idx_end = int(current_info["End"].iloc[0])
                idx_end = None if idx_end == -1 else idx_end
                motion_manip.cut_frame(idx_st, idx_end)
                self.idx_list_manip.append(idx_manip)
                self.hold_manip[idx_manip] = int(current_info["Hold1"].iloc[0])
                self.motion_dict_manip[idx_manip] = motion_manip

        self.variety = 0.3
        self.next_motion = None
        self.idx_next_motion = -1
        self.frm_hold = -1
        self.n_idle_played = len(self.idx_list_idle) // 2
        self.n_manip_played = len(self.idx_list_manip) // 2
        self.generate_next_idle_motion(is_first=True)

    def generate_next_idle_motion(self, is_first=False):
        self.current_motion = self.next_motion
        self.idx_current_motion = self.idx_next_motion
        """
        To do: Idle motion 생성 알고리즘 
        1. Idle to Idle
        2. KNN 랜덤 idle 넘어가는거 추가하기 
        3. 스트레칭 등의 랜덤 모션 추가
        """
        if not is_first:
            num = random.random()
            if num < self.variety and self.is_idle:
                self.generate_next_manipulator()
                return
        if len(self.idx_list_idle) < self.n_idle_played:
            self.idx_list_idle.append(self.idx_used_idle.popleft())
        idx_selected = random.randint(0, len(self.idx_list_idle) - 1)
        self.idx_next_motion = self.idx_list_idle.pop(idx_selected)
        self.next_motion = self.motion_dict_idle[self.idx_next_motion]
        self.idx_used_idle.append(self.idx_next_motion)

        self.is_idle = True

        if is_first:
            self.generate_next_idle_motion()

    def generate_next_manipulator(
        self,
    ):
        if len(self.idx_list_manip) < self.n_manip_played:
            self.idx_list_manip.append(self.idx_used_manip.popleft())
        idx_selected = random.randint(0, len(self.idx_list_manip) - 1)
        self.idx_next_motion = self.idx_list_manip.pop(idx_selected)
        self.next_motion = self.motion_dict_manip[self.idx_next_motion]
        self.frm_hold = self.hold_manip[self.idx_next_motion]
        self.idx_used_manip.append(self.idx_next_motion)
        self.is_idle = False
