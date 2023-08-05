from core.motion import Motion
from core.skeleton import Transform
from scipy.spatial.transform import Rotation as R


def append_end_motion(motion, count):
    frames = []
    for i in range(len(motion)):
        frame = motion[i].copy()
        frames.append(frame)
    for i in range(count):
        frames.append(motion[len(motion) - 1].copy())
    appended = Motion(
        motion.skeleton,
        frames,
        motion._frame_time,
        file_path=motion.file_path[:-4] + "_appended.bvh",
    )
    return appended


def slerp_test(motion, scale):
    frames = []
    for i in range(len(motion)):
        frame = motion[i].copy()
        frame._is_scalar = False
        original_trl = frame.get_root_transform().translation
        new_frame = frame.scale(scale, "slerp")
        new_trans = new_frame.get_root_transform()
        new_trans.translation = original_trl
        new_frame.set_root_transform(new_trans)
        original_trl_loc = frame.get_local_transform(0).translation
        new_frm_loc = new_frame.get_local_transform(0)
        new_frm_loc.translation = original_trl_loc
        new_frame.set_local_transform(0, new_frm_loc)
        frames.append(new_frame)
    rewinded_motion = Motion(
        motion.skeleton,
        frames,
        motion._frame_time,
        file_path=motion.file_path[:-4] + "_slerped.bvh",
    )
    return rewinded_motion


def rewinder(motion):
    frames = []
    for i in range(len(motion) - 1, -1, -1):
        frames.append(motion[i].copy())
    rewinded_motion = Motion(
        motion.skeleton,
        frames,
        motion._frame_time,
        file_path=motion.file_path[:-4] + "_rewind.bvh",
    )
    return rewinded_motion


def symmetric(motion):
    frames = []
    for i in range(len(motion)):
        frames.append(motion[i].copy())
    for i in range(len(motion) - 1, -1, -1):
        sym = motion[i].copy()
        # original = sym.get_local_transforms()
        # new_trans = []
        # for transform in original:
        #     angle = transform.rotation.as_euler("ZXY", degrees = True)
        #     angle[2] *= -1
        #     transform.rotation = R.from_euler("ZXY", angle, degrees=True)
        #     new_trans.append(transform)
        # sym.set_local_transforms(new_trans)
        frames.append(sym)
    rewinded_motion = Motion(
        motion.skeleton,
        frames,
        motion._frame_time,
        file_path=motion.file_path[:-4] + "_rewind.bvh",
    )
    return rewinded_motion


def body_vector_scaler_idle(motion, part, scale, idle_frame=None):
    frames = []
    if type(part) != int:
        part = motion[0].copy()._skeleton.joint_dict[part]

    if idle_frame is None:
        idle_frame = motion[0].copy()
    idle_rot = idle_frame.get_local_transform(part).rotation.as_rotvec()
    idle_trl = idle_frame.get_local_transform(part).translation
    for i in range(len(motion)):
        frame = motion[i].copy()
        part_trans = frame.get_local_transform(part)
        new_rot = R.from_rotvec(
            scale * (part_trans.rotation.as_rotvec() - idle_rot) + idle_rot
        )
        new_trls = scale * (part_trans.translation - idle_trl) + idle_trl
        new_trans = Transform(new_rot, new_trls)
        frame.set_local_transform(part, new_trans)
        frames.append(frame)
    scaled_motion = Motion(
        motion.skeleton,
        frames,
        motion._frame_time,
        file_path=motion.file_path[:-4] + "_scaled.bvh",
    )
    return scaled_motion


def body_vector_scaler(motion, part, scale):
    frames = []
    if type(part) != int:
        part = motion[0].copy()._skeleton.joint_dict[part]
    for i in range(len(motion)):
        frame = motion[i].copy()
        part_trans = frame.get_local_transform(part)
        new_rot = Transform(
            R.from_rotvec(scale * part_trans.rotation.as_rotvec()),
            scale * part_trans.translation,
        )
        frame.set_local_transform(part, new_rot)
        frames.append(frame)
    scaled_motion = Motion(
        motion.skeleton,
        frames,
        motion._frame_time,
        file_path=motion.file_path[:-4] + "_scaled.bvh",
    )
    return scaled_motion


def body_controller(motion, part, down_sign: int, angle: float, axis=1):
    axis = axis % 3
    if type(part) != int:
        part = motion[0].copy()._skeleton.joint_dict[part]
    for frame in motion:
        part_trans = frame.get_local_transform(part)
        if axis == 0:
            new_rot = part_trans.rotation * R.from_euler(
                "ZXY", [down_sign * angle, 0, 0], degrees=True
            )
        elif axis == 1:
            new_rot = part_trans.rotation * R.from_euler(
                "ZXY", [0, down_sign * angle, 0], degrees=True
            )
        elif axis == 2:
            new_rot = part_trans.rotation * R.from_euler(
                "ZXY", [0, 0, down_sign * angle], degrees=True
            )

        frame.set_local_rotation(part, new_rot)


def neck_controller(motion, down_sign: int, angle: float, axis=1):
    for frame in motion:
        neck_trans = frame.get_local_transform_by_name("Neck")
        # new_rot = neck_trans.rotation *  R.from_euler("ZXY",[0, down_sign * angle,0],  degrees=True)
        # new_rot = neck_trans.rotation *  R.from_euler("ZXY",[0, 0, down_sign * angle],  degrees=True)
        new_rot = neck_trans.rotation * R.from_euler(
            "ZXY", [down_sign * angle, 0, 0], degrees=True
        )
        frame.set_local_rotation_by_name("Neck", new_rot)


class speedController:
    def __init__(self) -> None:
        self.factor = 1.0

    def factor_setter(self, factor):
        self.factor = factor

    def assign_motion(self, motion: Motion):
        self.motion = motion
        self.slerp_list = []
        self.R_concat_list = []
        for i in range(len(self.motion)):
            current_frame = self.motion[i]
            local_transform = current_frame.get_local_transforms()
            if len(self.R_concat_list) == 0:
                for loci in enumerate(local_transform):
                    self.R

    # def quadratic_fitting(self, ):
    #     self.coeffs = []

    def linear_slerp(
        self,
    ):
        pass

    def changespeed(self, factor: float):
        self.factor = factor
        if self.factor == 1.0:
            return self._motion.copy()
        elif self.factor > 1:
            return self.fastforward(self.factor)
        else:
            return self.slowdown(self.factor)

    def fastforward(
        self,
    ):
        if self.factor < 1:
            raise Exception("ff factor must be greater than the 1")
        count = 0
        frames = []
        ff_path = self.motion.file_path[:-4] + "_ff.bvh"
        while count < len(self.motion):
            idx = int(count)
            if abs(count - idx) < 1e-6:
                frames.append(self.motion[idx])

            count += self.factor
        ff_motion = Motion(
            self.motion.skeleton, frames, self.motion._frame_time, ff_path
        )
        return ff_motion

    def slowdown(
        self,
    ):
        if self.factor > 1:
            raise Exception("sd factor must be greater than the 1")
