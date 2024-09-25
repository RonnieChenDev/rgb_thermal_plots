'''
canopy.py - module of files for canopy simulations

Student Name: 
Student ID  :

Version History:
    - 9/11/24 - original version released (temp_basecode.zip)
    - 11/9/24 - extended version released for tasks 3 & 4

'''
import random
import numpy as np
import matplotlib.pyplot as plt

class Tree():

    def __init__(self, pos, colour, size):
        self.pos = pos
        self.colour_code = colour
        self.size = size     # symmetrical, if noy, need height and width

    def get_image(self):
        s = self.size
        #print(s)
        img = np.ones((s,s)) * self.colour_code #row_y/col_x
        return img

    def get_coord(self):
        return self.pos

    def get_topleft(self):
        xleft = self.pos[0] - self.size//2
        ytop = self.pos[1] - self.size//2
        return (xleft,ytop)

    def get_size(self):
        return self.size

    def get_colour(self):
        return self.colour_code

    def set_size(self, size):
        self.size = size

    def set_colour(self, colour):
        self.colour_code = colour  # letter code for scatter plot

    def __str__(self):
        return f"Tree: {self.pos}"

class Block():

    def __init__(self, size, topleft):
        self.size = size        # size of Block square
        self.topleft = topleft  # (x,y) coord of topleft of Block
        self.items = []         # empty list to hold items

    def get_topleft(self):
        return self.topleft

    def add_item(self, item):
        self.items.append(item)

    def generate_image(self):
        grid = np.zeros((self.size,self.size)) # temporary grid for Block img

        for item in self.items:
            topleft = item.get_topleft() # topleft coord of item within Block
            img = item.get_image()       # 1D image of item (not 3D rgb)
            cx_start = topleft[0]          # x is columns
            ry_start = topleft[1]          # y is rows
            cx_stop = cx_start + img.shape[1]
            ry_stop = ry_start + img.shape[0]
            grid[ry_start:ry_stop,cx_start:cx_stop] = img[:,:] # overlay item on grid

        print(grid)
        return grid

    def __str__(self):
        return f"Block: {self.topleft}, #items = {len(self.items)}"

class House():

    def __init__(self, pos, colour, height, width):
        self.pos = pos
        self.colour_code = colour
        # self.size = size     # symmetrical, if noy, need height and width
        self.height = height
        self.width = width

    def get_image(self):
        # s = self.size
        #print(s)
        h = self.height
        w = self.width
        img = np.ones((h,w)) * self.colour_code #row_y/col_x
        return img

    def get_coord(self):
        return self.pos

    def get_topleft(self):
        xleft = self.pos[0] - self.width//2
        ytop = self.pos[1] - self.height//2
        return (xleft,ytop)

    #def get_size(self):
    #    return self.size

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_colour(self):
        return self.colour_code

    #def set_size(self, size):
    #    self.size = size

    def set_colour(self, colour):
        self.colour_code = colour  # letter code for scatter plot

    def __str__(self):
        return f"Tree: {self.pos}"
