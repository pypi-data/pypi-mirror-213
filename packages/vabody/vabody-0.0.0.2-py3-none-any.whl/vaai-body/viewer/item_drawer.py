from builtins import *
from copy import deepcopy

import numpy as np
import utilities.rendering_utils as ru
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *

from viewer.item_data import *


class ItemDrawer:
    def handling_class(self) -> object:
        """return handling class of this drawer"""
        pass

    def draw(self, item: object, frame: int, is_shadow: bool) -> void:
        """draw object"""
        pass

    def center(self, item: object, frame: int) -> np.array:
        """center position of item"""
        return None

    def num_of_frame(self, item: object) -> int:
        """number of frame of item"""
        return None


class FixedFrameDrawer(ItemDrawer):
    def __init__(self):
        pass

    def handling_data_name(self) -> str:
        """return handling name of this drawer"""
        return "Frame"

    def center(self, item: object) -> np.array:
        center = deepcopy(item.get_global_transform(0).translation)
        center[1] = 0.8
        return center

    def draw(self, item: object, color: list, is_shadow: bool, is_upper=False) -> void:
        if not is_shadow:
            self.draw_root(item.get_root_transform())
        ru.draw_fixed_skeleton(item._skeleton, item, color)

    def draw_root(self, root):
        ru.draw_transform(root)


class FrameDrawer(ItemDrawer):
    def __init__(self):
        pass

    def handling_data_name(self) -> str:
        """return handling name of this drawer"""
        return "Frame"

    def center(self, item: object) -> np.array:
        center = deepcopy(item.get_global_transform(0).translation)
        center[1] = 0.8
        return center

    def draw(self, item: object, color: list, is_shadow: bool, is_upper=False) -> void:
        if len(color) == 3:
            color.append(1.0)
        if not is_shadow:
            self.draw_root(item.get_root_transform())
        ru.draw_skeleton(item._skeleton, item, color, shape_type="line")

    def draw_root(self, root):
        pass
        # ru.draw_transform(root)


class PointDrawer(ItemDrawer):
    def __init__(self):
        pass

    def handling_data_name(self) -> str:
        """return handling name of this drawer"""
        return "Point"

    def draw(self, item: object, color: list, is_shadow: bool) -> void:
        if is_shadow:
            return

        if len(item) < 1:
            return

        draw_type = item.get_type()
        glPushMatrix()
        glTranslatef(*item.get_position())
        glColor3f(*color)
        if draw_type.lower() == "point":
            ru.draw_sphere(0.1)
        glPopMatrix()

    def center(self, item: object) -> np.array:
        center = deepcopy(item)
        center[1] = 0.8
        return center


class PointWithDirectionDrawer(ItemDrawer):
    def __init__(self):
        pass

    def handling_data_name(self) -> str:
        """return handling name of this drawer"""
        return "PointWithDirection"

    def draw(self, item: object, color: list, is_shadow: bool) -> void:
        if is_shadow:
            return

        glPushMatrix()
        glTranslatef(*item.position)
        glColor3f(*color)
        ru.draw_sphere(0.1)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(*item.direction)
        glEnd()
        glPopMatrix()

    def center(self, item: object) -> np.array:
        center = deepcopy(item)
        center[1] = 0.8
        return center


class Item:
    def __init__(
        self,
        data_object,
        color: list = [],
        alpha=1.0,
        name: str = "",
        selected: bool = False,
    ):
        self.data_object = data_object
        self._name = name
        self.selected = selected

        self.color = []
        for c in color:
            current_color = [*ru.Color.colors[c], alpha]
            self.color.append(current_color)

    def __iter__(self):
        return iter(self.data_object)

    def __len__(self):
        return len(self.data_object)

    def __getitem__(self, idx):
        return self.data_object[idx]

    def append(self, new_item):
        self.data_object.append(new_item)

    def num_frame(self):
        return len(self.data_object)

    def change_color(self, color, alpha=1.0):
        self.color = []
        for c in color:
            current_color = [*ru.Color.colors[c], alpha]
            self.color.append(current_color)
