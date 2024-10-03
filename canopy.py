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
import math

matplotlib.use('TKAgg')


class Item:
    def __init__(self, pos, colour_name, height, width, heat_capacity):
        self.pos = pos
        self.colour_name = colour_name  # colour_name like orange, pine_green... translate to RGB tuple by using utils.
        self.height = height
        self.width = width
        self.heat_capacity = float(heat_capacity)

    def get_image(self):
        h = int(self.height)
        w = int(self.width)
        img = np.ones((h, w, 3), dtype=np.uint8) * get_rgb_colour(self.colour_name)  # 3D RGB
        return img

    def get_coord(self):
        # central point coord of the item
        return self.pos

    def get_topleft(self):
        # While handling image, y-axis starting from 0 at the top of the image, instead of bottom.
        # X-axis starting from zero from left.
        # Top_left coord is not accurate when width or height is odd, as coord requires integer inputs.
        xleft = math.ceil(self.pos[0] - self.width / 2)
        ytop = math.ceil(self.pos[1] - self.height / 2)
        return xleft, ytop

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_colour(self):
        return self.colour_name

    def set_colour(self, colour_name):
        self.colour_name = colour_name

    def get_thermal_value(self, temperature):
        return self.heat_capacity * temperature


class Tree(Item):

    def __init__(self, pos, height, width, heat_capacity=4.0, colour_name='pine_green'):
        super().__init__(pos, colour_name, height, width, heat_capacity)

    def __str__(self):
        return f"Tree: {self.pos}"


class House(Item):

    def __init__(self, pos, height, width, heat_capacity=2, colour_name='orange'):
        super().__init__(pos, colour_name, height, width, heat_capacity)

    def __str__(self):
        return f"House: {self.pos}"


class Road(Item):
    # TODO: why height and width are invalid sometimes
    def __init__(self, pos, colour_name, heat_capacity, height=1, width=1):
        super().__init__(pos, colour_name, heat_capacity, height, width)

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
        if self.field_type == "park":
            self.block_bg_color = "pale_green"
        elif self.field_type == "yard":
            self.block_bg_color = "brown"
        else:
            raise ValueError(f"Invalid inputs for block_type: {self.field_type}. "
                             f"The expected value is either 'park' or 'yard'.")

    def get_topleft(self):
        return self.topleft

    def is_occupied(self, x, y):
        return self.occupied_loc[y, x]

    def bulk_mark_as_occupied(self, points):
        for x, y in points:
            self.occupied_loc[y, x] = True

    def mark_as_occupied(self, x, y):
        self.occupied_loc[y, x] = True

    def add_item(self, item):
        self.items.append(item)

    def add_road(self):
        # make sure the start point is at the left top corner
        start_point = (random.randint(2, self.size // 2), random.randint(2, self.size // 2))
        points = []
        mark_points = []
        if random.randint(1, 10) > 5:
            # horizontal line
            for x in range(start_point[0], min(start_point[0] + random.randint(5, 15), self.size - 1)):
                points.append((x, start_point[1]))
                # consider road width is 1 and mark the whole points in a road
                for w in range(1 + 1):
                    mark_points.append((x, start_point[1] + w))
        else:
            # vertical line
            for y in range(start_point[1], min(start_point[1] + random.randint(5, 15), self.size - 1)):
                points.append((start_point[0], y))
                # consider road width is 1 and mark the whole points in a road
                for w in range(1 + 1):
                    mark_points.append((start_point[0] + w, y))

        # Add the coord of each element road in the line to occupied list. Include the width
        self.bulk_mark_as_occupied(mark_points)

        # Add road. Thermal property and colour_name differ when it's in park or yard.
        for point in points:
            if self.field_type == 'park':
                self.add_item(Road(pos=point, colour_name='light_grey', heat_capacity=1.5))
            elif self.field_type == 'yard':
                self.add_item(Road(pos=point, colour_name='grey', heat_capacity=1))
            else:
                raise ValueError(f"Invalid inputs for block_type: {self.field_type}. "
                                 f"The expected value is either 'park' or 'yard'.")

    # TODO: height or length naming, and overlapping coord fix
    def add_house(self, house_length, house_width):
        house_x = 0
        house_y = 0
        house_coord_search_done = False
        while house_coord_search_done is not True:
            # random generate a coord for house, and compare with existing occupied coord
            house_x = random.randint(0, self.size - house_length)
            house_y = random.randint(0, self.size - house_width)

            not_occupied_house_coord = True
            house_points = []
            for i in range(house_x, (house_x + house_length)):
                for j in range(house_y, (house_y + house_width)):
                    house_points.append((i, j))
                    if self.is_occupied(i, j):
                        not_occupied_house_coord = False
            if not_occupied_house_coord:
                self.bulk_mark_as_occupied(house_points)
                house_coord_search_done = True

        self.add_item(House(pos=(house_x, house_y), height=house_length, width=house_width))

    def add_trees(self, field_type):
        quantity_of_trees = 0
        if field_type == 'park':
            quantity_of_trees = random.randint(25, 30)
        elif field_type == 'yard':
            quantity_of_trees = random.randint(15, 20)
        trees_points = []
        for _ in range(quantity_of_trees):
            tree_x = random.randint(0, self.size - 1)
            tree_y = random.randint(0, self.size - 1)

            if not self.is_occupied(tree_x, tree_y):
                trees_points.append((tree_x, tree_y))

        self.bulk_mark_as_occupied(trees_points)
        for tree in trees_points:
            self.add_item(Tree(pos=tree, height=1, width=1))

    def generate_block_image(self):
        bg_rgb_colour = get_rgb_colour(self.block_bg_color)
        grid = np.ones((self.size, self.size, 3), dtype=np.uint8) * bg_rgb_colour  # 3D RGB grid, preset bg colour

        for item in self.items:
            topleft = item.get_topleft()  # topleft coord of item within Block
            img = item.get_image()  # 3D RGB image
            cx_start = max(0, int(topleft[0]))  # x is columns
            ry_start = max(0, int(topleft[1]))  # y is rows
            cx_stop = min(self.size, int(cx_start + img.shape[1]))
            ry_stop = min(self.size, int(ry_start + img.shape[0]))

            img_height = ry_stop - ry_start
            img_width = cx_stop - cx_start

            print(f"Topleft: {topleft}, img shape: {img.shape}, grid shape: {grid.shape}")
            print(f"Placing image from ({ry_start}:{ry_stop}, {cx_start}:{cx_stop})")

            if img_height > 0 and img_width > 0:
                grid[ry_start:ry_stop, cx_start:cx_stop, :] = img[:img_height, :img_width, :]  # overlay item on grid
            else:
                print(f"Invalid slice: start ({cx_start}, {ry_start}), stop ({cx_stop}, {ry_stop})")

        return grid

    def generate_thermal_image(self):
        ...

    def __str__(self):
        return f"Block: {self.topleft}, #items = {len(self.items)}"


class Map:
    def __init__(self, rgb_blocks, thermal_blocks, map_config, temperature=25):
        self.rgb_blocks = rgb_blocks
        self.thermal_blocks = thermal_blocks
        self.block_size = map_config['block_size']
        self.block_row_num = map_config['block_row_num']
        self.block_col_num = map_config['block_col_num']
        self.block_num = map_config['block_num']
        self.map_shape = map_config['map_shape']
        self.park_limit = map_config['park_limit']
        self.temperature = temperature

    def get_env_temperature(self):
        return self.temperature

    def generate_rgb_view(self, rgb_blocks, map_config):
        map_image = np.zeros((self.map_shape[0] * self.block_size, self.map_shape[1] * self.block_size, 3),
                             dtype=np.uint8)
        for block in rgb_blocks:
            block_img = block.generate_block_image()
            topleft = block.get_topleft()

            x_start, y_start = topleft
            x_end = x_start + block_img.shape[1]
            y_end = y_start + block_img.shape[0]
            map_image[y_start:y_end, x_start:x_end, :] = block_img
        return map_image

    def generate_thermal_view(self):
        map_area = []
        for block in self.blocks:
            map_area.append(block.generate_thermal_image())
        return np.array(map_area)
