import numpy as np
from scipy.spatial.transform import Rotation as R


class Transform:
    __slots__ = ("_rotation", "_rotation_np", "_translation")

    def __init__(self, rotation=np.identity(3), translation=np.zeros(3)):
        if type(rotation) == np.ndarray:
            self._rotation_np = rotation
            self._rotation = None
        elif type(rotation) == R:
            self._rotation_np = None
            self._rotation = rotation
        else:
            print("rotation type error : {}".format(type(rotation)))
            exit(1)
        self._translation = np.array(translation)

    @property
    def rotation(self):
        if self._rotation is None:
            self._rotation = R.from_matrix(self.rotation_np)
        return self._rotation

    @property
    def rotation_np(self):
        if self._rotation_np is None:
            self._rotation_np = self.rotation.as_matrix()
        return self._rotation_np

    @property
    def translation(self):
        return self._translation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        self._rotation_np = None

    @rotation_np.setter
    def rotation_np(self, value):
        self._rotation_np = value
        self._rotation = None

    @translation.setter
    def translation(self, value):
        self._translation = np.array(value)

    def __mul__(self, transform):
        new_orientation = self.rotation * transform.rotation
        new_translation = self._translation + self.rotation.apply(transform.translation)
        return Transform(new_orientation, new_translation)

    def apply(self, vector):
        return self.rotation.apply(vector) + self._translation

    def inverse(self):
        rot_inv = self.rotation.inv()
        return Transform(rot_inv, -rot_inv.apply(self._translation))

    def __getitem__(self, idx):
        if self.rotation.single:
            print("single instance error")
            exit(1)
        return Transform(self.rotation_np[idx], self._translation[idx])

    def __len__(self):
        if self.rotation.single:
            return 1
        return len(self._rotation)


class Joint:
    def __init__(self, name, parent, dof, idx, offset=np.zeros(3)):
        self._name = name
        self._default_offset = offset
        self._default_transform = Transform(translation=self._default_offset)
        self._parent = parent
        if self._parent is not None:
            self._parent.add_child(self)
        self._children = []
        self._dof = dof
        self._idx = idx
        self._body_transform = Transform()
        self._body_height = 0.0
        self._body_radius = 0.0

        self._is_end = False
        self._end_site_transform = Transform()
        # self._idx_in_skeleton

    def __str__(self):
        parent_name = None
        if self._parent is not None:
            parent_name = self._parent.name
        return "Joint {} - parent : {}, dof : {}".format(
            self._name, parent_name, self._dof
        )

    def add_child(self, child):
        self._children.append(child)

    def set_end(self, end_site_transform):
        self._is_end = True
        self._end_site_transform = end_site_transform

    @property
    def body_transform(self):
        return self._body_transform

    @body_transform.setter
    def body_transform(self, new_transform):
        self._body_transform = new_transform

    @property
    def name(self):
        return self._name

    @property
    def default_offset(self):
        return self._default_offset

    @property
    def default_transform(self):
        return self._default_transform

    @property
    def dof(self):
        return self._dof

    @property
    def idx(self):
        return self._idx

    @property
    def idx_in_skeleton(self):
        return self._idx_in_skeleton

    @idx_in_skeleton.setter
    def idx_in_skeleton(self, value):
        self._idx_in_skeleton = value

    @property
    def parent(self):
        return self._parent

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def global_pose_orientation(self):
        return self._global_pose_orientation

    @global_pose_orientation.setter
    def global_pose_orientation(self, value):
        self._global_pose_orientation = value

    @property
    def global_pose_translation(self):
        return self._global_pose_translation

    @global_pose_translation.setter
    def global_pose_translation(self, value):
        self._global_pose_translation = value


class Skeleton:
    def __init__(self, name="Unnamed"):
        self._name = name
        # joint order - joint dict, should be sorted?
        # joint hierarchy
        # joint

        self._joint_dict = {}  # {name: index}
        self._joints = []
        self._frame_time = 1.0 / 30.0
        self._dof = 0
        self._rot = "ZXY"

    @property
    def name(self):
        return self._name

    @property
    def joints(self):
        return self._joints

    @property
    def joint_dict(self):
        return self._joint_dict

    def get_joint_by_name(self, name):
        return self._joints[self._joint_dict[name]]

    def num_joints(self):
        return len(self._joints)

    def load_hierarchy_from_bvh(self, file_path):
        self._joint_dict = {}
        self._joints = []

        with open(file_path, "r") as bvh:  # parse bvh file
            name = None
            joint_stack = [None]
            is_end = False

            for line in bvh.readlines():
                line = line.strip()

                if line[:4].upper() == "ROOT" or line[:5].upper() == "JOINT":
                    name = line.split(" ")[1]

                elif line[:6].upper() == "OFFSET":
                    # offset coordinate?
                    _, x, y, z = line.split(" ")
                    x, y, z = float(x), float(y), float(z)
                    offset = np.array([x, y, z]) / 100.0
                    if is_end:
                        self._joints[-1].set_end(Transform(translation=offset))

                elif line[:8].upper() == "CHANNELS":
                    # TODO for translation channels
                    num_channel = int(line.split(" ")[1])
                    split_line = line.split()
                    self._rot = (
                        split_line[-3][0].upper()
                        + split_line[-2][0].upper()
                        + split_line[-1][0].upper()
                    )
                    parent_name = joint_stack[-2]
                    parent = None
                    if parent_name is not None:
                        parent = self._joints[self._joint_dict[parent_name]]
                    self._joints.append(
                        Joint(name, parent, num_channel, len(self._joints), offset)
                    )
                    self._joint_dict[name] = len(self._joints) - 1

                elif line[:8].upper() == "END SITE":
                    is_end = True

                elif line[0] == "{":
                    joint_stack.append(name)

                elif line[0] == "}":
                    is_end = False
                    joint_stack.pop()

                elif line[:10].upper() == "FRAME TIME":
                    _, time = line.split(":")
                    time = float(time.strip())
                    self._frame_time = time
                    break

        self._dof = 0
        for joint in self._joints:
            joint.idx_in_skeleton = self._dof
            self._dof += joint.dof

            # compute body
            # TODO : body construction for end site
            if len(joint._children) > 0:
                child_mean_pose = np.zeros(3)
                for child in joint._children:
                    child_mean_pose += child.default_transform.translation
                child_mean_pose /= len(joint._children)
                center = child_mean_pose / 2

                if np.linalg.norm(center) < 1e-6:
                    dir_from_parent = joint.default_transform.translation
                    dir_from_parent = dir_from_parent / (
                        np.linalg.norm(dir_from_parent) + 1e-6
                    )
                    center = dir_from_parent * 0.05
                    height = 0.1
                else:
                    height = np.linalg.norm(child_mean_pose)

            else:
                end_pose = joint._end_site_transform.translation
                if np.linalg.norm(end_pose) < 1e-6:
                    dir_from_parent = joint.default_transform.translation
                    dir_from_parent = dir_from_parent / (
                        np.linalg.norm(dir_from_parent) + 1e-6
                    )

                    center = dir_from_parent * 0.05
                    height = 0.1
                else:
                    center = end_pose * 0.05
                    height = np.linalg.norm(end_pose)

            axis_y = center
            axis_y = (
                np.array([0, 1, 0])
                if np.linalg.norm(axis_y) < 1e-6
                else axis_y / np.linalg.norm(axis_y)
            )
            axis_x = np.array([1, 0, 0])
            if np.linalg.norm(np.cross(axis_x, axis_y)) < 1e-6:
                axis_x = np.array([0, 0, 1])
            axis_z = np.cross(axis_x, axis_y)
            axis_z = axis_z / np.linalg.norm(axis_z)

            axis_x = np.cross(axis_y, axis_z)
            axis_x = axis_x / np.linalg.norm(axis_x)

            rotation = np.stack([axis_x, axis_y, axis_z], axis=-1)
            joint.body_transform.rotation_np = rotation
            joint.body_transform.translation = center
            # TODO : body definition
            joint._body_height = height
            joint._body_radius = 0.05
