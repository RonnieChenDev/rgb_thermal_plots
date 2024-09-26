"""
canopy.py - module of files for canopy simulations

Student Name: Xi CHEN
Student ID  : 22278096

Version History:
    - 9/11/24 - original version released (temp_basecode.zip)
    - 11/9/24 - extended version released for tasks 3 & 4
    - 13/9/24 - add House class for PracTest3
"""
# import random
import numpy as np


# import matplotlib.pyplot as plt


class Item:
    def __init__(self, pos, colour, length, width, heat_capacity):
        self.pos = pos
        self.colour = colour
        self.width = width
        self.length = length
        self.heat_capacity = heat_capacity

    def get_image(self):
        h = self.length
        w = self.width
        img = np.ones((h, w)) * self.colour
        return img

    def get_coord(self):
        return self.pos

    def get_topleft(self):
        xleft = self.pos[0] - self.width // 2
        ytop = self.pos[1] - self.length // 2
        return (xleft, ytop)

    def get_length(self):
        return self.length

    def get_width(self):
        return self.width

    def get_colour(self):
        return self.colour

    def set_colour(self, colour):
        self.colour = colour  # letter code for scatter plot

    def get_thermal_value(self, temparature):
        return self.heat_capacity * temparature


class Tree(Item):

    def __init__(self, pos, colour, length, width, heat_capacity):
        super().__init__(pos, colour, length, width, heat_capacity)

    def __str__(self):
        return f"Tree: {self.pos}"


class House(Item):

    def __init__(self, pos, colour, length, width, heat_capacity):
        super().__init__(pos, colour, length, width, heat_capacity)

    def __str__(self):
        return f"House: {self.pos}"


class Road(Item):

    def __init__(self, pos, colour, length, width, heat_capacity):
        super().__init__(pos, colour, length, width, heat_capacity)

    def __str__(self):
        return f"Road: {self.pos}"


class Block():

    def __init__(self, size, topleft):
        self.size = size  # size of Block square
        self.topleft = topleft  # (x,y) coord of topleft of Block
        self.items = []  # empty list to hold items

    def get_topleft(self):
        return self.topleft

    def add_item(self, item):
        self.items.append(item)

    def generate_image(self):
        grid = np.zeros((self.size, self.size))  # temporary grid for Block img

        for item in self.items:
            topleft = item.get_topleft()  # topleft coord of item within Block
            img = item.get_image()  # 1D image of item (not 3D rgb)
            cx_start = topleft[0]  # x is columns
            ry_start = topleft[1]  # y is rows
            cx_stop = cx_start + img.shape[1]
            ry_stop = ry_start + img.shape[0]
            grid[ry_start:ry_stop, cx_start:cx_stop] = img[:, :]  # overlay item on grid

        print(grid)
        return grid

    def generate_thermal_image(self):
        ...

    def __str__(self):
        return f"Block: {self.topleft}, #items = {len(self.items)}"


class Map():
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
