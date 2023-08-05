import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp

from vaaibody.core.skeleton import Transform

# Here we need root blending code


class RootBlender:
    def __init__(self, src, dst, dur_cnt, is_moving=False):
        self.dur_cnt = dur_cnt
        self.src_transform = src.get_root_transform()
        self.dst_transform = dst.get_root_transform()
        self.moving_flag = is_moving
        left_foot = (
            src.get_component_translation_by_name("LeftToe")
            - dst.get_component_translation_by_name("LeftToe")
        ) / 2
        right_foot = (
            src.get_component_translation_by_name("RightToe")
            - dst.get_component_translation_by_name("RightToe")
        ) / 2
        self.transl_int = np.matmul(
            src.get_root_transform().rotation_np, (left_foot + right_foot)
        )
        self.transl_offset = (
            self.src_transform.translation
            - self.dst_transform.translation
            + self.transl_int
        )

        R_concat = R.concatenate(
            [self.src_transform.rotation, self.dst_transform.rotation]
        )
        st_end = [0, dur_cnt]
        self.slerp = Slerp(st_end, R_concat)

    def change_transl_offset(self, translation):
        self.transl_offset = translation

    def linear_ori_blending(self, frame, cnt):
        times = [cnt]
        R_concat = R.concatenate(
            [self.src_transform.rotation, frame.get_root_transform().rotation]
        )
        st_end = [0, self.dur_cnt]
        slerp = Slerp(st_end, R_concat)
        interp_rots = slerp(times)
        return interp_rots

    def root_ori_blending(self, cnt):
        times = [cnt]
        interp_rots = self.slerp(times)
        return interp_rots

    def root_trans_blending(self, cnt):
        translate = (
            self.src_transform.translation * (self.dur_cnt - cnt)
            + self.dst_transform.translation * cnt
        )
        translate /= self.dur_cnt
        return translate

    def root_transl_off(self, cnt):
        translate = (
            self.src_transform.translation + self.transl_int * cnt / self.dur_cnt
        )
        return translate

    def root_moving_off(self, frame, cnt):
        return (
            frame.get_root_transform().translation
            + (self.transl_offset - self.transl_int)
            + self.transl_int * cnt / self.dur_cnt
        )

    def root_blending(self, frame, cnt):
        if cnt < self.dur_cnt:
            if self.moving_flag:
                root_ori = self.linear_ori_blending(frame, cnt)[0]
                transl = self.root_moving_off(frame, cnt)
            else:
                root_ori = self.root_ori_blending(cnt)[0]
                transl = self.root_transl_off(cnt)
        else:
            root_ori = frame.get_root_transform().rotation
            transl = frame.get_root_transform().translation + self.transl_offset
        new_root = Transform(root_ori, transl)
        frame.set_root_transform(new_root)
        return frame

    def root_loop_blending(self, frame, cnt):
        if cnt < self.dur_cnt:
            root_ori = self.root_ori_blending(cnt)[0]
            transl = self.root_trans_blending(cnt)
        else:
            root_ori = frame.get_root_transform().rotation
            transl = frame.get_root_transform().translation
        new_root = Transform(root_ori, transl)
        frame.set_root_transform(new_root)
        return frame

    def linear_root_blending(self, frame, cnt):
        ori_blendings = self.linear_ori_blending(frame, cnt)
        root_ori = ori_blendings[0]
        trans = frame.get_root_transform().translation
        new_root = Transform(root_ori, trans)
        frame.set_root_transform(new_root)
        return frame


class RootInertialization:
    def __init__(
        self,
        source_first,
        source_second,
        target,
        blend_len,
        is_moving=False,
        frame_time=1 / 60,
    ):
        self._blend_len = blend_len
        self._frame_time = frame_time
        self.moving_flag = is_moving

        self._q0 = (
            target.get_root_transform().inverse() * source_first.get_root_transform()
        )
        self._qp = (
            target.get_root_transform().inverse() * source_second.get_root_transform()
        )

        self.default_transl_offset = (
            source_first.get_root_transform().translation
            - target.get_root_transform().translation
        )
        left_foot0 = (
            source_first.get_component_translation_by_name("LeftToe")
            - target.get_component_translation_by_name("LeftToe")
        ) / 2
        right_foot0 = (
            source_first.get_component_translation_by_name("RightToe")
            - target.get_component_translation_by_name("RightToe")
        ) / 2
        self.transl0 = np.matmul(
            source_first.get_root_transform().rotation_np, (left_foot0 + right_foot0)
        )
        left_footp = (
            source_second.get_component_translation_by_name("LeftToe")
            - target.get_component_translation_by_name("LeftToe")
        ) / 2
        right_footp = (
            source_second.get_component_translation_by_name("RightToe")
            - target.get_component_translation_by_name("RightToe")
        ) / 2
        translp = np.matmul(
            source_second.get_root_transform().rotation_np, (left_footp + right_footp)
        )
        self.transl_offset = self.default_transl_offset + self.transl0

        self._x0 = np.array([self._q0.rotation.as_rotvec()])
        self._x0[np.linalg.norm(self._x0, axis=1) == 0, :] = 0.00000001
        self._x0_u = self._x0 / np.linalg.norm(self._x0, axis=1, keepdims=True)
        self._x0_u[np.isnan(self._x0_u)] = 0.0
        self._x0 = np.linalg.norm(self._x0, axis=1)
        xp = []
        qpj = self._qp.rotation.as_quat()
        xp.append(2 * np.arctan(np.dot(qpj[:3], self._x0_u[0]) / qpj[3]))
        xp = np.array(xp)

        self._x0_t = np.array([self.transl0])
        self._x0_t[np.linalg.norm(self._x0_t, axis=1) == 0, :] = 0.00000001
        self._x0_t_u = self._x0_t / np.linalg.norm(self._x0_t, axis=1, keepdims=True)
        self._x0_t_u[np.isnan(self._x0_t_u)] = 0.0
        self._x0_t = np.linalg.norm(self._x0_t, axis=1)
        xp_t = []

        qpj_t = translp
        xp_t.append(np.dot(qpj_t, self._x0_t_u[0]))
        xp_t = np.array(xp_t)
        # print(self._x0_t_u, xp_t)

        self._x0_u = np.concatenate([self._x0_u, self._x0_t_u], axis=0)
        self._x0 = np.concatenate([self._x0, self._x0_t], axis=0)
        xp = np.concatenate([xp, xp_t], axis=0)

        self._v0 = (self._x0 - xp) / frame_time
        t1 = np.array([blend_len * frame_time for j in range(self._x0.shape[0])])
        self._a0 = (-8 * self._v0 * t1 - 20 * self._x0) / (t1**2)
        self._A = (
            -1
            * (self._a0 * t1**2 + 6 * self._v0 * t1 + 12 * self._x0)
            / (2 * t1**5)
        )
        self._B = (3 * self._a0 * t1**2 + 16 * self._v0 * t1 + 30 * self._x0) / (
            2 * t1**4
        )
        self._C = (
            -1
            * (3 * self._a0 * t1**2 + 12 * self._v0 * t1 + 20 * self._x0)
            / (2 * t1**3)
        )

    def get_xt(self, count):
        t = self._frame_time * count
        xt = (
            self._A * t**5
            + self._B * t**4
            + self._C * t**3
            + 0.5 * self._a0 * t**2
            + self._v0 * t
            + self._x0
        )
        xt = xt.reshape(-1, 1) * self._x0_u

        joint_num = int(xt.shape[0] / 2)
        xt_r = xt[:joint_num]
        xt_t = xt[joint_num:]
        return R.from_rotvec(xt_r), xt_t

    def root_blending(self, frame, count):
        xt_r, xt_t = self.get_xt(count)
        if count < self._blend_len:
            root_ori = xt_r[0] * frame.get_root_transform().rotation
            transl = (
                frame.get_root_transform().translation
                + self.default_transl_offset
                + (self.transl0 - xt_t)[0]
            )
        else:
            root_ori = frame.get_root_transform().rotation
            transl = (
                frame.get_root_transform().translation
                + self.default_transl_offset
                + self.transl0
            )
        new_root = Transform(root_ori, transl)
        frame.set_root_transform(new_root)
        return frame


class BlendingInertialization:
    def __init__(
        self,
        source_first,
        source_second,
        target,
        blend_len,
        frame_time=1 / 30,
        blending_front=True,
        is_frame=False,
        moving_target=None,
        target_vel=None,
        target_acc=None,
        vel_reducer=None,
    ):
        """
        Args
            source_first: Frame, 앞 모션의 blending 직전 Frame (t-1)
            source_second: Frame, 앞 모션의 blending 직전-1 Frame (t-2)
            target: Frame or Motion, 타겟
            blend_len: Int, 얼마 길이동안 blending 할건지 #frames 로 주어짐
            frame_time: 1/fps
            is_frame: Frame blending인지 여부
            moving_target: (Optional) Frame, is_frame인 경우 moving inertialization인 경우
            target_vel: (Optional) Frame, is_frame인 경우 끝의 motion의 velocity 계산을 위한 target +1 frame
            target_acc: (Optional) Frame, is_frame인 경우 끝의 motion의 acceleration 계산을 위한 target +2 frame
        """
        self._blend_len = blend_len
        self._frame_time = frame_time
        self._blending_front = blending_front
        self._is_frame = is_frame

        self._start = 0 if blending_front else target.num_frame() - 1
        self._end = (
            blend_len if blending_front else target.num_frame() - (blend_len + 1)
        )

        self.vel_thresh = np.pi / 8
        self.acc_thresh = np.pi / 4

        if is_frame:
            self._q0 = (source_first - target).get_local_transforms()
            self._qp = (source_second - target).get_local_transforms()
        else:
            self.new_motion = target.copy()
            self._q0 = (source_first - target[self._start]).get_local_transforms()
            self._qp = (source_second - target[self._start]).get_local_transforms()
        """
        First, Inertializing Quaternion
        x0_u: Axis 
        x0: Angle
        xp ==> x-1: 2tan-1 (q_xyz * x0 . q_w)
        """
        self._x0 = np.array(
            [self._q0[j].rotation.as_rotvec() for j in range(len(self._q0))]
        )
        self._x0[np.linalg.norm(self._x0, axis=1) == 0, :] = 0.00000001
        self._x0_u = self._x0 / np.linalg.norm(self._x0, axis=1, keepdims=True)
        self._x0_u[np.isnan(self._x0_u)] = 0.0
        self._x0 = np.linalg.norm(self._x0, axis=1)

        xp = []
        for j in range(len(self._qp)):
            qpj = self._qp[j].rotation.as_quat()
            xp.append(2 * np.arctan(np.dot(qpj[:3], self._x0_u[j]) / qpj[3]))
        xp = np.array(xp)
        len_xp = xp.shape[0]
        """
        This is translation part, inertializing vector
        """
        self._x0_t = np.array([self._q0[j].translation for j in range(len(self._q0))])
        self._x0_t[np.linalg.norm(self._x0_t, axis=1) == 0, :] = 1e-7
        self._x0_t_u = self._x0_t / np.linalg.norm(self._x0_t, axis=1, keepdims=True)
        self._x0_t_u[np.isnan(self._x0_t_u)] = 0.0
        self._x0_t[np.linalg.norm(self._x0_t, axis=1) < 1e-6, :] = 0
        self._x0_t = np.linalg.norm(self._x0_t, axis=1)
        xp_t = []
        for j in range(len(self._qp)):
            qpj_t = self._qp[j].translation
            xp_t.append(np.dot(qpj_t, self._x0_t_u[j]))

        self._x0_u = np.concatenate([self._x0_u, self._x0_t_u], axis=0)

        self._x0 = np.concatenate([self._x0, self._x0_t], axis=0)
        xp = np.concatenate([xp, xp_t], axis=0)
        self._v0 = (self._x0 - xp) / frame_time
        if vel_reducer is not None:
            red_scale = 1.0
            q_red = (vel_reducer - target).get_local_transforms()
            x_red = []
            for j in range(len(q_red)):
                qredj = q_red[j].rotation.as_quat()
                x_red.append(2 * np.arctan(np.dot(qredj[:3], self._x0_u[j]) / qredj[3]))
            x_red = np.array(x_red) / frame_time
            self._v0[:len_xp] = self._v0[:len_xp] - red_scale * x_red

        self._v0[:len_xp] = np.clip(
            self._v0[:len_xp], a_min=None, a_max=self.vel_thresh
        )
        t1 = np.array(
            [
                min(
                    blend_len * self._frame_time,
                    -5 * self._x0[j] / (self._v0[j] - 1e-10),
                )
                for j in range(self._x0.shape[0])
            ]
        )
        t1[t1 < 1e-5] = blend_len * self._frame_time
        self.t1 = t1
        # t1 = np.array([blend_len * frame_time for j in range(self._x0.shape[0])])

        """
        This part is for initializing v1 and a1
        원래는 끝의 Frame에서 v1 = 0 , a1 = 0를 가정하고 문제를 품
        즉, 
        f(t1) = 0
        f'(t1) = 0
        f''(t1) = 0
        f'''(t1) = 0 (Jerk = 0, 이것을 통해서 a0의 값을 설정한 것임)
        5차 함수 Inertialization fitting이다.

        하지만, 여기서 Frame +1, Frame +2 를 제공한 경우
        f(t1) = 0
        f'(t1) = v1
        f''(t1) = a1
        f'''(t1) = 0 (Jerk = 0, 이것을 통해서 a0의 값을 설정한 것임)
        5차 함수 Inertialization fitting 으로 가정하고 문제를 풀 수 있다.        
        """
        self._v1 = 0
        self._a1 = 0
        apply_v1_flag = False
        apply_a1_flag = False
        if is_frame:
            if target_vel is not None:
                if moving_target is None:
                    moving_target = target
                qdiff = (moving_target - target).get_local_transforms()
                qv = (target_vel - target).get_local_transforms()
                apply_v1_flag = True
                if target_acc is not None:
                    qa = (target_acc - target).get_local_transforms()
                    apply_a1_flag = True
        else:
            qdiff = (target[self._start] - target[self._start]).get_local_transforms()
            qv = (target[self._start + 1] - target[self._start]).get_local_transforms()
            qa = (target[self._start + 2] - target[self._start]).get_local_transforms()
            apply_v1_flag = True
            apply_a1_flag = True

        if apply_v1_flag:
            xdiff = []
            xv = []
            for j in range(len(qdiff)):
                qdiffj = qdiff[j].rotation.as_quat()
                xdiff.append(
                    2 * np.arctan(np.dot(qdiffj[:3], self._x0_u[j]) / qdiffj[3])
                )
            for j in range(len(qv)):
                qvj = qv[j].rotation.as_quat()
                xv.append(2 * np.arctan(np.dot(qvj[:3], self._x0_u[j]) / qvj[3]))
            xdiff = np.array(xdiff)
            xv = np.array(xv)

            transl_idx = self._x0_u.shape[0] // 2
            xdiff_t = []
            xv_t = []
            for j in range(len(qdiff)):
                qdiffj_t = qdiff[j].translation
                xdiff_t.append(np.dot(qdiffj_t, self._x0_u[j + transl_idx]))
            for j in range(len(qv)):
                qvj_t = qv[j].translation
                xv_t.append(np.dot(qvj_t, self._x0_u[j + transl_idx]))
            xdiff = np.concatenate([xdiff, xdiff_t], axis=0)
            xv = np.concatenate([xv, xv_t], axis=0)
            diff = xv - xdiff
            self._v1 = diff / self._frame_time
            self._v1[:len_xp] = np.clip(
                self._v1[:len_xp], a_min=None, a_max=np.abs(self._v0)[:len_xp]
            )

        if apply_a1_flag:
            xa = []
            for j in range(len(qa)):
                qaj = qa[j].rotation.as_quat()
                xa.append(2 * np.arctan(np.dot(qaj[:3], self._x0_u[j]) / qaj[3]))
            xa = np.array(xa)
            xa_t = []
            for j in range(len(qa)):
                qaj_t = qa[j].translation
                xa_t.append(np.dot(qaj_t, self._x0_u[j + transl_idx]))
            xa = np.concatenate([xa, xa_t], axis=0)
            diff = xa + xdiff - 2 * xv
            diff = np.where(diff > np.pi / 2, diff - np.pi, diff)
            diff = np.where(diff < -np.pi / 2, diff + np.pi, diff)
            self._a1 = diff / (self._frame_time**2)
            """
            여기서 0< blending duration <= 1 이라고 가정하고 
            a1 = k * v1 이라는 가정을 통해 트릭을 쓴다.
            결론부터 말하면, -11 < k < 3 인 경우 residual 방정식이 허근을 갖게 되어
            t = min (t1, -5 * x0 / v0) 를 사용할 수 있게 된다.
            그러면 if v1 < 0 이면
            3 * v1 < a1 < -11 * v1 이고,
            v1 > 0 이면
            -11 * v1 < a1 < 3 * v1 이다.
            마지막으로, 보수적으로, acc_thresh와 비교해서,
            a1 < min(acc_thresh, max_clip) 로 둔다.
            """
            min_clip = np.where(self._v1 > 0, -10 * self._v1, 2.8 * self._v1)
            max_clip = np.where(self._v1 > 0, 2.8 * self._v1, -10 * self._v1)
            max_clip = np.where(max_clip > self.acc_thresh, self.acc_thresh, max_clip)
            self._a1[:len_xp] = np.clip(
                self._a1[:len_xp], a_min=min_clip[:len_xp], a_max=max_clip[:len_xp]
            )

        """
        Set the constants that satisfies above equations
        """
        self._a0 = (
            3 * self._a1 * t1**2 - (8 * self._v0 + 12 * self._v1) * t1 - 20 * self._x0
        ) / (t1**2)
        self._a0[:len_xp] = np.clip(self._a0[:len_xp], a_min=None, a_max=0)

        self._A = (
            -1
            * (
                (self._a0 - self._a1) * t1**2
                + (6 * self._v0 + 6 * self._v1) * t1
                + 12 * self._x0
            )
            / (2 * t1**5)
        )
        self._B = (
            (3 * self._a0 - 2 * self._a1) * t1**2
            + (16 * self._v0 + 14 * self._v1) * t1
            + 30 * self._x0
        ) / (2 * t1**4)
        self._C = (
            -1
            * (
                (3 * self._a0 - self._a1) * t1**2
                + (12 * self._v0 + 8 * self._v1) * t1
                + 20 * self._x0
            )
            / (2 * t1**3)
        )

    def apply_blending(self):
        if self._is_frame:
            raise Exception(f"Use frame blending")

        _A = self._A
        _B = self._B
        _C = self._C
        _a0 = self._a0
        _v0 = self._v0
        _x0 = self._x0
        _x0_u = self._x0_u

        t1 = self.t1
        for idx_blend in range(self._blend_len):
            xt_r, xt_t = self.get_xt(idx_blend, _A, _B, _C, _a0, _v0, _x0, _x0_u, t1)
            self.new_motion[idx_blend].add_local_transforms(xt_r, xt_t)

        return self.new_motion

    def get_xt(self, count, _A, _B, _C, _a0, _v0, _x0, _x0_u, t1):
        t = self._frame_time * count
        t = np.where(t1 < t, t1, t)
        xt = (
            _A * t**5 + _B * t**4 + _C * t**3 + 0.5 * _a0 * t**2 + _v0 * t + _x0
        )
        xt = xt.reshape(-1, 1) * _x0_u

        joint_num = int(xt.shape[0] / 2)
        xt_r = xt[:joint_num]
        xt_t = xt[joint_num:]
        return R.from_rotvec(xt_r), xt_t

    def apply_frame_blending(self, frame, count):
        if not self._is_frame:
            raise Exception(f"Use motion blending")
        _A = self._A
        _B = self._B
        _C = self._C
        _a0 = self._a0
        _v0 = self._v0
        _x0 = self._x0
        _x0_u = self._x0_u

        t1 = self.t1
        xt_r, xt_t = self.get_xt(count, _A, _B, _C, _a0, _v0, _x0, _x0_u, t1)

        frame.add_local_transforms(xt_r, xt_t)
        return frame


# Joint level blender for frames
class JointBlendingInertialization:
    def __init__(
        self,
        joint_name,
        source_first,
        source_second,
        target,
        blend_len,
        frame_time=1 / 30,
        blending_front=True,
    ):
        self._joint_name = joint_name
        self._blend_len = blend_len
        self._frame_time = frame_time
        self._blending_front = blending_front

        self._start = 0 if blending_front else target.num_frame() - 1
        self._end = (
            blend_len if blending_front else target.num_frame() - (blend_len + 1)
        )

        self._q0 = (source_first - target).get_local_transform_by_name(self._joint_name)
        self._qp = (source_second - target).get_local_transform_by_name(
            self._joint_name
        )

        self._x0 = np.array([self._q0.rotation.as_rotvec()])
        self._x0[np.linalg.norm(self._x0, axis=1) == 0, :] = 0.00000001
        self._x0_u = self._x0 / np.linalg.norm(self._x0, axis=1, keepdims=True)
        self._x0_u[np.isnan(self._x0_u)] = 0.0
        self._x0 = np.linalg.norm(self._x0, axis=1)
        xp = []
        qpj = self._qp.rotation.as_quat()
        xp.append(2 * np.arctan(np.dot(qpj[:3], self._x0_u[0]) / qpj[3]))
        xp = np.array(xp)

        self._x0_t = np.array([self._q0.translation])
        self._x0_t[np.linalg.norm(self._x0_t, axis=1) == 0, :] = 0.00000001
        self._x0_t_u = self._x0_t / np.linalg.norm(self._x0_t, axis=1, keepdims=True)
        self._x0_t_u[np.isnan(self._x0_t_u)] = 0.0
        self._x0_t = np.linalg.norm(self._x0_t, axis=1)
        xp_t = []

        qpj_t = self._qp.translation
        xp_t.append(np.dot(qpj_t, self._x0_t_u[0]))
        xp_t = np.array(xp_t)

        self._x0_u = np.concatenate([self._x0_u, self._x0_t_u], axis=0)
        self._x0 = np.concatenate([self._x0, self._x0_t], axis=0)
        xp = np.concatenate([xp, xp_t], axis=0)

        self._v0 = (self._x0 - xp) / frame_time
        t1 = np.array([blend_len * frame_time for j in range(self._x0.shape[0])])
        self._a0 = (-8 * self._v0 * t1 - 20 * self._x0) / (t1**2)
        self._A = (
            -1
            * (self._a0 * t1**2 + 6 * self._v0 * t1 + 12 * self._x0)
            / (2 * t1**5)
        )
        self._B = (3 * self._a0 * t1**2 + 16 * self._v0 * t1 + 30 * self._x0) / (
            2 * t1**4
        )
        self._C = (
            -1
            * (3 * self._a0 * t1**2 + 12 * self._v0 * t1 + 20 * self._x0)
            / (2 * t1**3)
        )

    def get_xt(self, count):
        t = self._frame_time * count
        xt = (
            self._A * t**5
            + self._B * t**4
            + self._C * t**3
            + 0.5 * self._a0 * t**2
            + self._v0 * t
            + self._x0
        )
        xt = xt.reshape(-1, 1) * self._x0_u

        joint_num = int(xt.shape[0] / 2)
        xt_r = xt[:joint_num]
        xt_t = xt[joint_num:]
        return R.from_rotvec(xt_r[0]), xt_t[0]

    def apply_frame_blending(self, frame, count):
        xt_r, xt_t = self.get_xt(count)
        frame.add_local_transform_by_name(self._joint_name, Transform(xt_r, xt_t))
        return frame
