"""
canopy.py - module of files for canopy simulations

Student Name: Xi CHEN
Student ID  : 22278096

Version History:
    - 9/11/24 - original version released (temp_basecode.zip)
    - 11/9/24 - extended version released for tasks 3 & 4
    - 13/9/24 - add House class for PracTest3
    - 27/9/24 - modify the image generation from 1d image to 3d rgb image
"""
import random
import numpy as np
import matplotlib
from utils import *

matplotlib.use('TKAgg')


class Item:
    def __init__(self, pos, colour_name, length, width, heat_capacity):
        self.pos = pos
        self.colour_name = colour_name  # colour_name like orange, pine_green... translate to RGB tuple by using utils.
        self.width = width
        self.length = length
        self.heat_capacity = heat_capacity

    def get_image(self):
        h = self.length
        w = self.width
        img = np.ones((h, w, 3), dtype=np.uint8) * get_rgb_colour(self.colour_name)  # 3D RGB
        return img

    def get_coord(self):
        return self.pos

    def get_topleft(self):
        xleft = self.pos[0] - self.width // 2
        ytop = self.pos[1] - self.length // 2
        return xleft, ytop

    def get_length(self):
        return self.length

    def get_width(self):
        return self.width

    def get_colour(self):
        return self.colour

    def set_colour(self, colour):
        self.colour = colour

    def get_thermal_value(self, temperature):
        return self.heat_capacity * temperature


class Tree(Item):

    def __init__(self, pos, heat_capacity=5.0, colour_name='pine_green', length=2, width=2):
        super().__init__(pos, colour_name, length, width, heat_capacity)

    def __str__(self):
        return f"Tree: {self.pos}"


class House(Item):

    def __init__(self, pos, heat_capacity=2.0, colour_name='orange', length=6, width=4):
        super().__init__(pos, colour_name, length, width, heat_capacity)

    def __str__(self):
        return f"House: {self.pos}"


class Road(Item):

    def __init__(self, pos, heat_capacity=1.0, colour_name='grey', length=5, width=5):
        super().__init__(pos, colour_name, length, width, heat_capacity)

    def __str__(self):
        return f"Road: {self.pos}"


class Block:

    def __init__(self, size, topleft, field_type):
        self.size = size  # Block is in square by default
        self.topleft = topleft  # (x,y) coord of topleft of Block
        self.items = []  # empty list to hold items
        self.occupied_loc = np.zeros((size, size), dtype=bool)
        self.field_type = field_type

        # bg color for blocks, depends on the input block_type.
        # park and yard are the available options, otherwise it throws exception.
        if field_type == "park":
            self.block_bg_color = "pale_green"
        elif field_type == "yard":
            self.block_bg_color = "brown"
        else:
            raise ValueError(f"Invalid inputs for block_type: {field_type}. "
                             f"The expected value is either 'park' or 'yard'.")

    def get_topleft(self):
        return self.topleft

    def is_occupied(self, x, y):
        return self.occupied_loc[x, y]

    def add_item(self, item):
        x, y = item.pos
        # if self.is_occupied(x, y):
        #     raise ValueError(f"Position ({x},{y}) is already occupied.")
        # self.occupied_loc[x, y] = True
        self.items.append(item)

    def generate_image(self):
        bg_rgb_colour = get_rgb_colour(self.block_bg_color)
        grid = np.ones((self.size, self.size, 3), dtype=np.uint8) * bg_rgb_colour  # 3D RGB grid, preset bg colour

        for item in self.items:
            topleft = item.get_topleft()  # topleft coord of item within Block
            img = item.get_image()  # 3D RGB image
            cx_start = topleft[0]  # x is columns
            ry_start = topleft[1]  # y is rows
            cx_stop = cx_start + img.shape[1]
            ry_stop = ry_start + img.shape[0]
            grid[ry_start:ry_stop, cx_start:cx_stop, :] = img[:, :, :]  # overlay item on grid

        print(grid)
        return grid

    def generate_thermal_image(self):
        ...

    def __str__(self):
        return f"Block: {self.topleft}, #items = {len(self.items)}"


class Map:
    def __init__(self, blocks):
        self.blocks = blocks

    def generate_rgb_view(self):
        map_area = []
        for block in self.blocks:
            map_area.append(block.generate_image())
        return np.array(map_area)

    def generate_thermal_view(self):
        map_area = []
        for block in self.blocks:
            map_area.append(block.generate_thermal_image())
        return np.array(map_area)
