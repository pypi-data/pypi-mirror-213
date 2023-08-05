from core.audio import *
from core.skeleton import *
from core.motion import MotionDatabase
from module.nontalking_control_module import NonTalkingModule
from testing.motion_tester import *
from testing.blending_test_vis import TestWindow
from testing.convAI_viewer_test import ConvAIWindow

"""
여기에 testing 파일을 덤프하여 테스트해본다.
"""

"""
Test 1. diff character test
data/motion/ 에 KTG_01 만들고
Minio  vaai-body/230118_Body_KTG/Total_BVH 있는 파일 다 옮기기

작동 코드
    skeleton_original = Skeleton(name="KTG")
    skeleton_original.load_hierarchy_from_bvh("data/motion/KTG_01/VAAI_Non_E_01_de_01.bvh")
    skeleton_retarget = Skeleton(name="LJY")
    skeleton_retarget.load_hierarchy_from_bvh("data/motion/Gesture_Before/VAAI_Basic_01_01.bvh")
    db_path = "data/motion/KTG_01/"
    diff_character_test(skeleton_original, skeleton_retarget, db_path)

파란 캐릭터: KTG 캐릭터
반투명 붉은 캐릭터: KTG 캐릭터의 모션을 KSW Skeleton에 입힌 결과
"""

"""
    actor_name = "HSO_02"
    skeleton = Skeleton(name=actor_name)
    skeleton.load_hierarchy_from_bvh(
        "data/motion/" + actor_name + "/VAAI_Non_E_01_de_01.bvh"
    )
    db = MotionDatabase(skeleton, "data/motion/" + actor_name + "/")
    # phase_db = MotionDatabase(skeleton, "data/motion/" + actor_name + "_phase/")
    test_window = TestWindow(skeleton, db)
    test_window.loop()
"""

"""
    actor_name = "HSO_02"
    skeleton = Skeleton(name=actor_name)
    skeleton.load_hierarchy_from_bvh(
        "data/motion/" + actor_name + "/VAAI_Non_E_01_de_01.bvh"
    )
    db = MotionDatabase(skeleton, "data/motion/" + actor_name + "/")
    non_talking_module = NonTalkingMotion(db)
    test_window = ConvAIWindow(skeleton, non_talking_module)
    test_window.loop()

"""
"""
    actor_name = "HSO_02"
    skeleton = Skeleton(name=actor_name)
    skeleton.load_hierarchy_from_bvh(
        "data/motion/" + actor_name + "/VAAI_Non_E_01_de_01.bvh"
    )
    db = MotionDatabase(skeleton, "data/motion/" + actor_name + "_conv/", use_npz=True)
    # non_talking_module = NonTalkingMotion(db)
    non_talking_module = NonTalkingModule(db)
    test_window = ConvAIWindow(skeleton, non_talking_module)
    test_window.loop()
"""

if __name__ == "__main__":
    actor_name = "HSO_02_conv"
    skeleton = Skeleton(name=actor_name)
    skeleton.load_hierarchy_from_bvh(
        "/home/yoonhee/Downloads" + "/VAAI_Non_E_01_de_01.bvh"
    )
    db = MotionDatabase(skeleton, "data/motion/" + actor_name + "/", use_npz=True)
    non_talking_module = NonTalkingModule(db)
    test_window = ConvAIWindow(skeleton, non_talking_module)
    test_window.loop()
