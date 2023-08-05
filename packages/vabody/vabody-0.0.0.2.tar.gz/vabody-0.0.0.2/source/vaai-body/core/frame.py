from copy import deepcopy
from typing import List, Optional

import numpy as np
from collections import deque # deque 패키지 불러오기

import scipy as sp
from scipy.spatial.transform import Rotation as R
from utilities.timechecker import TimeChecker as TC

from .skeleton import Skeleton, Transform



class Frame:
    __slots__ = (
        "_skeleton",
        "_root_transform",
        "_root_transform_inv",
        "_local_transforms",
        "_global_transforms",
        "_component_transforms",
        "_body_global_transforms",
        "_is_scalar",
        "_rot",
        "_global_dirty_flags",
        "_component_dirty_flags",
        "_body_global_dirty_flags",
    )

    def __init__(
        self,
        skeleton: Skeleton,
        root_transform: Transform,
        local_transforms: List[Transform],
        root_transform_inv: Optional[Transform] = None,
        global_transforms: Optional[List[Transform]] = None,
        component_transforms: Optional[List[Transform]] = None,
        body_global_transforms: Optional[List[Transform]] = None,
        scalar=True,
    ):
        self._skeleton = skeleton
        self._root_transform = root_transform
        self._root_transform_inv = root_transform_inv
        self._local_transforms = local_transforms
        self._global_transforms = global_transforms
        self._component_transforms = component_transforms
        self._body_global_transforms = body_global_transforms
        self._is_scalar = scalar

        self._rot = self._skeleton._rot
        self._global_dirty_flags = [False for _ in range(self._skeleton.num_joints())]
        self._component_dirty_flags = [False for _ in range(self._skeleton.num_joints())]
        self._body_global_dirty_flags = [False for _ in range(self._skeleton.num_joints())]

        if global_transforms is None:
            self._global_transforms = [None] * self._skeleton.num_joints()
        if component_transforms is None:
            self._body_global_transforms = [None] * self._skeleton.num_joints()
        if body_global_transforms is None:
            self._component_transforms = [None] * self._skeleton.num_joints()

    def get_raw_frame(
        self,
    ):
        raw_frames = []
        global_trans = self.get_root_transform() * self.get_local_transform(0)
        translate = global_trans.translation * 100
        rotate = global_trans.rotation.as_euler(self._rot, degrees=True)
        raw_frames.append(translate[0])
        raw_frames.append(translate[1])
        raw_frames.append(translate[2])
        raw_frames.append(rotate[0])
        raw_frames.append(rotate[1])
        raw_frames.append(rotate[2])

        local = self.get_local_transforms()
        for i, loci in enumerate(local):
            if i == 0:
                continue
            degree = loci.rotation.as_euler(self._rot, degrees=True)
            raw_frames.append(degree[0])
            raw_frames.append(degree[1])
            raw_frames.append(degree[2])
        return raw_frames

    def copy(self):
        new_frame = Frame(
            self._skeleton,
            deepcopy(self._root_transform),
            deepcopy(self._local_transforms),
            scalar=self._is_scalar,
        )
        return new_frame

    def fast_copy(
        self,
    ):
        new_frame = Frame(
            self._skeleton,
            deepcopy(self._root_transform),
            deepcopy(self._local_transforms),
            scalar=self._is_scalar,
        )
        return new_frame

    def get_root_transform(self):
        return self._root_transform

    def get_inverse_root_transform(self):
        if self._root_transform_inv is None:
            self._root_transform_inv = self._root_transform.inverse()
        return self._root_transform_inv

    def num_joints(self):
        return self._skeleton.num_joints()

    def get_local_transforms(self):
        return self._local_transforms

    def get_local_transform(self, joint_idx):
        return self._local_transforms[joint_idx]

    def get_local_transform_by_name(self, joint_name):
        return self.get_local_transform(self._skeleton.joint_dict[joint_name])

    def get_local_rotation(self, joint_idx):
        return self._local_transforms[joint_idx].rotation

    def get_local_rotation_by_name(self, joint_name):
        return self.get_local_rotation(self._skeleton.joint_dict[joint_name])

    def get_local_translation(self, joint_idx):
        return self._local_transforms[joint_idx].translation

    def get_local_translation_by_name(self, joint_name):
        return self.get_local_translation(self._skeleton.joint_dict[joint_name])

    def get_body_global_transform(self, joint_idx):
        if self._body_global_dirty_flags[joint_idx] or self._body_global_transforms[joint_idx] is None:
            self.update_transforms(joint_idx, update_type='body_global')
        return self._body_global_transforms[joint_idx]

    def get_body_global_transform_by_name(self, joint_name):
        return self.get_body_global_transform(self._skeleton.joint_dict[joint_name])

    def get_global_transform(self, joint_idx):
        if self._global_dirty_flags[joint_idx] or self._global_transforms[joint_idx] is None:
            self.update_transforms(joint_idx, update_type='global')
        return self._global_transforms[joint_idx]

    def get_relative_translation_by_name(self, joint1, joint2):
        diff = self.get_global_translation_by_name(
            joint1
        ) - self.get_global_translation_by_name(joint2)
        norm_diff = np.matmul(
            np.linalg.inv(self.get_global_rotation_by_name(joint2).as_matrix()), diff
        )
        return norm_diff

    def get_relative_translation(self, joint1, joint2):
        diff = self.get_global_translation(joint1) - self.get_global_translation(joint2)
        norm_diff = np.matmul(
            np.linalg.inv(self.get_global_rotation(joint2).as_matrix()), diff
        )
        return norm_diff

    def get_global_transform_by_name(self, joint_name):
        return self.get_global_transform(self._skeleton.joint_dict[joint_name])

    def get_global_rotation(self, joint_idx):
        return self.get_global_transform(joint_idx).rotation

    def get_global_rotation_by_name(self, joint_name):
        return self.get_global_rotation(self._skeleton.joint_dict[joint_name])

    def get_global_translation(self, joint_idx):
        return self.get_global_transform(joint_idx).translation

    def get_global_translation_by_name(self, joint_name):
        return self.get_global_translation(self._skeleton.joint_dict[joint_name])

    def get_component_transform(self, joint_idx):
        if self._component_dirty_flags[joint_idx] or self._component_dirty_flags[joint_idx] is None:
            self.update_transforms(joint_idx, update_type='component')
        return self._component_transforms[joint_idx]

    def get_component_transform_by_name(self, joint_name):
        if joint_name[-2:] == "_e":
            joint_idx = self._skeleton.joint_dict[joint_name[:-2]]
            joint_comp = self.get_component_transform(joint_idx)
            end_local_transform = self._skeleton.joints[joint_idx]._end_site_transform
            end_comp_transform = joint_comp * end_local_transform
            return end_comp_transform
        return self.get_component_transform(self._skeleton.joint_dict[joint_name])

    def get_component_translation(self, joint_idx):
        return self.get_component_transform(joint_idx).translation

    def get_component_translation_by_name(self, joint_name):
        return self.get_component_transform_by_name(joint_name).translation

    def set_root_transform(self, new_transform):
        self._root_transform = new_transform
        self._root_transform_inv = self._root_transform.inverse()
        self.set_dirty(0) 

    def set_by_raw_rotations(self, raw_rotations):
        for idx in range(1, self.num_joints()):
            current_rotation = R.from_euler(
                self._rot, raw_rotations[3 * (idx + 1) : 3 * (idx + 2)], degrees=True
            )
            self.set_local_rotation(joint_idx=idx, new_rotation=current_rotation)

    def set_local_transforms(self, new_transforms):
        for idx in range(self.num_joints()):
            self.set_local_transform(idx, new_transforms[idx])

    def set_local_transform_by_name(self, joint_name, new_transform):
        self.set_local_transform(
            self._skeleton.joint_dict[joint_name], new_transform
        )

    def set_local_transform(self, joint_idx, new_transform):
        self._local_transforms[joint_idx] = new_transform
        self.set_dirty(joint_idx)

    def set_local_translation(self, joint_idx, new_translation):
        self._local_transforms[joint_idx].translation = new_translation
        self.set_dirty(joint_idx)

    def set_local_translation_by_name(self, joint_name, new_translation):
        self.set_local_translation(
            self._skeleton.joint_dict[joint_name], new_translation
        )

    def set_local_rotation(self, joint_idx, new_rotation):
        self._local_transforms[joint_idx].rotation = new_rotation
        self.set_dirty(joint_idx)

    def set_local_rotation_by_name(self, joint_name, new_rotation):
        joint_idx = self._skeleton.joint_dict[joint_name]
        self._local_transforms[joint_idx].rotation = new_rotation
        self.set_dirty(joint_idx)

    def set_frame(self, new_frame):
        self.set_root_transform(new_frame.get_root_transform())
        self.set_local_transforms(new_frame.get_local_transforms())

    def set_dirty(self, joint_idx):
        joint_dict = self._skeleton.joint_dict
        self._component_dirty_flags[joint_idx] = True
        self._global_dirty_flags[joint_idx] = True
        self._body_global_dirty_flags[joint_idx] = True

        # original version - traverse all joint idx
        # for i in range(joint_idx, self._skeleton.num_joints()):
        #     if self._skeleton.joints[i].parent is None:
        #         continue
        #     if self._dirty_flags[self._skeleton.joints[i].parent.idx]:
        #         self._dirty_flags[i] = True

        # new version
        # traverse only child node
        visited = []
        need_to_visit = deque()
        need_to_visit.append(self._skeleton.joints[joint_idx])

        while need_to_visit:
            node = need_to_visit.pop()
            visit_joint_idx = joint_dict[node.name]
            if visit_joint_idx not in visited:
                self._component_dirty_flags[visit_joint_idx] = True
                self._global_dirty_flags[visit_joint_idx] = True
                self._body_global_dirty_flags[visit_joint_idx] = True
                visited.append(visit_joint_idx)
                need_to_visit.extend(node._children)

    def update_transforms(self, joint_idx, update_type='global'):
        joint = self._skeleton.joints[joint_idx]
        parent = joint.parent

        if self._global_dirty_flags[joint_idx]:
            if parent is not None:
                self._global_transforms[joint_idx] = (
                    self.get_global_transform(parent.idx)
                    * self._local_transforms[joint_idx]
                )
            else:
                self._global_transforms[joint_idx] = (
                    self._root_transform * self._local_transforms[joint_idx]
                )
            self._global_dirty_flags[joint_idx] = False

        if update_type == 'body_global' and self._body_global_dirty_flags[joint_idx]:
            self._body_global_transforms[joint_idx] = (
                self._global_transforms[joint_idx] * joint.body_transform
            )
            self._body_global_dirty_flags[joint_idx] = False

        elif update_type == 'component' and self._component_dirty_flags[joint_idx]:
            self._component_transforms[joint_idx] = (
                self.get_inverse_root_transform() * self._global_transforms[joint_idx]
            )
            self._component_dirty_flags[joint_idx] = False

    def scale(self, scale, method="vector"):
        if method == "vector":
            return self.scale_vector(scale)
        elif method == "slerp":
            return self.scale_slerp(scale)
        else:
            return self.scale_vector(scale)

    def scale_body(self, scale, part, method="vector"):
        if type(part) != int:
            part = self._skeleton.joint_dict[part]
        if method == "vector":
            return self.scale_vector_body(scale, part)
        elif method == "slerp":
            return self.scale_slerp_body(scale, part)
        else:
            return self.scale_vector_body(scale, part)

    def scale_vector(self, scale):
        if self._is_scalar:
            raise Exception("Type Error (scale): " + self + " is a scalar")
        new_root = Transform(
            R.from_rotvec(scale * self.get_root_transform().rotation.as_rotvec()),
            scale * self.get_root_transform().translation,
        )
        new_joints = []
        for j in range(self.num_joints()):
            new_joints.append(
                Transform(
                    R.from_rotvec(
                        scale * self.get_local_transform(j).rotation.as_rotvec()
                    ),
                    scale * self.get_local_transform(j).translation,
                )
            )
        return Frame(self._skeleton, new_root, new_joints, scalar=False)

    def scale_slerp(self, scale):
        if self._is_scalar:
            raise Exception("Type Error (scale): " + self + " is a scalar")
        slerp_root = Transform(
            sp.spatial.transform.Slerp(
                [0.0, 1.0],
                R.from_matrix(
                    [
                        R.identity().as_matrix(),
                        self.get_root_transform().rotation.as_matrix(),
                    ]
                ),
            )([scale])[0],
            scale * self.get_root_transform().translation,
        )
        slerp_joints = []
        for j in range(self.num_joints()):
            slerp_joints.append(
                Transform(
                    sp.spatial.transform.Slerp(
                        [0.0, 1.0],
                        R.from_matrix(
                            [
                                Transform().rotation.as_matrix(),
                                self.get_local_transform(j).rotation.as_matrix(),
                            ]
                        ),
                    )([scale])[0],
                    scale * self.get_local_transform(j).translation,
                )
            )
        return Frame(self._skeleton, slerp_root, slerp_joints, scalar=False)

    def scale_vector_body(self, scale, part):
        if self._is_scalar:
            raise Exception("Type Error (scale): " + self + " is a scalar")
        new_root = self.get_root_transform()
        new_joints = []
        for j in range(self.num_joints()):
            if j == part:
                new_joints.append(
                    Transform(
                        R.from_rotvec(
                            scale * self.get_local_transform(j).rotation.as_rotvec()
                        ),
                        scale * self.get_local_transform(j).translation,
                    )
                )
            else:
                new_joints.append(self.get_local_transform(j))
        return Frame(self._skeleton, new_root, new_joints, scalar=False)

    def scale_slerp_body(self, scale, part):
        if self._is_scalar:
            raise Exception("Type Error (scale): " + self + " is a scalar")
        slerp_root = self.get_root_transform()
        slerp_joints = []
        for j in range(self.num_joints()):
            if j == part:
                slerp_joints.append(
                    Transform(
                        sp.spatial.transform.Slerp(
                            [0.0, 1.0],
                            R.from_matrix(
                                [
                                    Transform().rotation.as_matrix(),
                                    self.get_local_transform(j).rotation.as_matrix(),
                                ]
                            ),
                        )([scale])[0],
                        scale * self.get_local_transform(j).translation,
                    )
                )
            else:
                slerp_joints.append(self.get_local_transform(j))
        return Frame(self._skeleton, slerp_root, slerp_joints, scalar=False)

    def global_move(self, diff):
        self.set_root_transform(diff * self.get_root_transform())

    def local_move(self, diff):
        self.set_root_transform(self.get_root_transform() * diff)

    def add_local_transform(self, idx, diff_transform):
        self.set_local_transform(idx, self.get_local_transform(idx) * diff_transform)

    def add_local_transform_by_name(self, joint_name, diff_transform):
        self.add_local_transform(self._skeleton.joint_dict[joint_name], diff_transform)

    def add_local_transforms(self, diff_rotation=None, diff_translation=None):
        for idx in range(self.num_joints()):
            self.add_local_transform(
                idx,
                Transform(
                    diff_rotation[idx] if diff_rotation is not None else np.identity(3),
                    diff_translation[idx]
                    if diff_translation is not None
                    else np.zeros(3),
                ),
            )

    def update_root_raw(
        self,
    ):
        self.init_raw_frames()
        global_trans = self.get_root_transform() * self.get_local_transform(0)
        translate = global_trans.translation * 100
        self._raw_frames[0] = translate[0]
        self._raw_frames[1] = translate[1]
        self._raw_frames[2] = translate[2]
        self.update_rot_raw_frames(0, global_trans.rotation)

        # rotate = global_trans.rotation.as_euler(self._rot, degrees=True)
        # self._raw_frames[3] = rotate[0]
        # self._raw_frames[4] = rotate[1]
        # self._raw_frames[5] = rotate[2]

    def update_rot_raw_frames(self, joint_idx, rotation):
        self.init_raw_frames()
        degree = rotation.as_euler(self._rot, degrees=True)
        self._raw_frames[3 * joint_idx + 3] = degree[0]
        self._raw_frames[3 * joint_idx + 4] = degree[1]
        self._raw_frames[3 * joint_idx + 5] = degree[2]

    def __add__(self, move):
        if move._is_scalar:
            raise Exception("Type Error (__add__): scalar")
        new_root_transform = self.get_root_transform()
        # new_root_transform = self.get_root_transform() * move.get_root_transform()
        # new_root_transform.translation = self.get_root_transform().translation + move.get_root_transform().translation
        new_local_transforms = [
            self.get_local_transform(j) * move.get_local_transform(j)
            for j in range(self.num_joints())
        ]
        return Frame(self._skeleton, new_root_transform, new_local_transforms)

    def __sub__(self, base_frame):
        new_root_transform = self.get_root_transform()
        # new_root_transform = base_frame.get_root_transform().inverse() * self.get_root_transform()
        # new_root_transform.translation = self.get_root_transform().translation - base_frame.get_root_transform().translation
        new_local_transforms = [
            base_frame.get_local_transform(j).inverse() * self.get_local_transform(j)
            for j in range(self.num_joints())
        ]
        return Frame(
            self._skeleton, new_root_transform, new_local_transforms, scalar=False
        )