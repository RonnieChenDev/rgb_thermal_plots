"""
    cano.py - module of files for canopy simulations, modified based on the version of my outcome of PracTest3.

    Student Name: Xi CHEN
    Student ID  : 22278096
"""
import random
import matplotlib
from utils import *
import math

matplotlib.use('TKAgg')


class Item:
    def __init__(self, pos, colour_name, height, width, heat_capacity, item_temperature=15):
        self.pos = pos
        self.colour_name = colour_name  # colour_name like orange, pine_green... translate to RGB tuple by using utils.
        self.height = height
        self.width = width
        self.heat_capacity = float(heat_capacity)
        self.item_temperature = float(item_temperature)  # all the items are having same initial temperature
        self.mass = self.height * self.width

    def get_image(self):
        """
        Generate each item image with RGB value in np list.
        :return: img
        """
        h = int(self.height)
        w = int(self.width)
        img = np.ones((h, w, 3), dtype=np.uint8) * get_rgb_colour(self.colour_name)  # 3D RGB
        return img

    def get_coord(self):
        """
        Get central point coord of the item.
        :return: pos
        """
        return self.pos

    def get_topleft(self):
        """
        While handling image, y-axis starting from 0 at the top of the image, instead of bottom.
        X-axis starting from zero from left.
        Top_left coord is not accurate when width or height is odd, as coord requires integer inputs.
        :return: topleft coord of item
        """
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

    def get_updated_temperature(self, env_temperature):
        """
        Calculate updated temperature of item based on mass, environment temperature,
        item current temperature and heat capacity of the item. n controls if it looks smooth in the plots.
        :param env_temperature:
        :return: updated item temperature
        """
        n = 2
        try:
            temp_diff = 2 * (float(env_temperature) - self.item_temperature) / (self.mass * self.heat_capacity * n)
            self.item_temperature += temp_diff
            return self.item_temperature
        except (ValueError, ZeroDivisionError) as e:
            if self.mass * self.heat_capacity * n == 0:
                raise ZeroDivisionError(f"Divide 0 error, please check mass and heat_capacity: {e}")
            else:
                raise ValueError(f"Failed to convert env_temperature, please check! {e}")


class Tree(Item):

    def __init__(self, pos, height, width, heat_capacity=4.5, colour_name='pine_green'):
        super().__init__(pos, colour_name, height, width, heat_capacity)
        # add more weight for trees' mass.
        self.mass = self.height * self.width * 2.5

    def __str__(self):
        return f"Tree: {self.pos}"


class House(Item):

    def __init__(self, pos, height, width, heat_capacity=3, colour_name='orange'):
        super().__init__(pos, colour_name, height, width, heat_capacity)
        # decrease weight for house, more than road
        self.mass = self.height * self.width * 0.3

    def __str__(self):
        return f"House: {self.pos}"


class Road(Item):
    def __init__(self, pos, colour_name, heat_capacity, height, width):
        super().__init__(pos, colour_name, heat_capacity, height, width)
        # decrease weight for roads
        self.mass = self.height * self.width * 0.8

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
        """
        Validate if the input coord is already in use.
        :param x:
        :param y:
        :return: flag of judging if it is already occupied
        """
        return self.occupied_loc[y, x]

    def bulk_mark_as_occupied(self, points):
        """
        Mark points as occupied in bulk.
        :param points:
        :return:
        """
        for x, y in points:
            self.occupied_loc[y, x] = True

    def mark_as_occupied(self, x, y):
        """
        Mark a point as occupied independently.
        :param x:
        :param y:
        :return:
        """
        self.occupied_loc[y, x] = True

    def add_item(self, item):
        self.items.append(item)

    def add_road(self, road_height, road_width):
        """
        Add road to a block. Road consists of several Road objects in a horizontal or vertical line.
        No need to check occupied status for their coord before adding tp block as it should always invoke firstly.
        :param road_height:
        :param road_width:
        :return:
        """
        # make sure the start point is at the left top corner
        start_point = (random.randint(2, self.size // 2), random.randint(2, self.size // 2))
        points = []
        mark_points = []

        # random to get True or False
        if random.randint(1, 10) > 5:
            # horizontal line
            # make sure it will not go over the boundary.
            for x in range(start_point[0], min(start_point[0] + random.randint(5, 15), self.size - 1)):
                points.append((x, start_point[1]))
                # consider road width is 1 and mark the whole points in a road
                for w in range(road_width + 1):
                    mark_points.append((x, start_point[1] + w))
                    mark_points.append((x, start_point[1] - w))
        else:
            # vertical line
            for y in range(start_point[1], min(start_point[1] + random.randint(5, 15), self.size - 1)):
                points.append((start_point[0], y))
                # consider road width is 1 and mark the whole points in a road
                for w in range(road_width + 1):
                    mark_points.append((start_point[0] + w, y))
                    mark_points.append((start_point[0] - w, y))

        # Add the coord of each element road in the line to occupied list. Include the width
        self.bulk_mark_as_occupied(mark_points)

        # Add road. Thermal property and colour_name differ when it's in park or yard.
        for point in points:
            if self.field_type == 'park':
                self.add_item(Road(pos=point, colour_name='light_grey', heat_capacity=1.5,
                                   height=road_height, width=road_width))
            elif self.field_type == 'yard':
                self.add_item(Road(pos=point, colour_name='grey', heat_capacity=1,
                                   height=road_height, width=road_width))
            else:
                raise ValueError(f"Invalid inputs for block_type: {self.field_type}. "
                                 f"The expected value is either 'park' or 'yard'.")

    def add_house(self, house_height, house_width):
        """
        Add house to a block. Need check for coord is occupied or not before adding.
        :param house_height:
        :param house_width:
        :return:
        """
        # central coord of house item
        house_x = 0
        house_y = 0
        house_coord_search_done = False
        while house_coord_search_done is not True:
            # random generate a coord for house, and compare with existing occupied coord
            # use floor divide to make the random range smaller, in case over the boundary
            # minus 1 in case it generates right on the boundary of block
            house_x = random.randint(math.ceil(house_width / 2), math.floor(self.size - house_width / 2) - 1)
            house_y = random.randint(math.ceil(house_height / 2), math.floor(self.size - house_height / 2) - 1)

            not_occupied_house_coord = True
            house_points = []
            # here use floor and ceil divide to the boundary to occupy larger area in case any issue
            # plus 1 to include the right boundary of range to the loop
            for i in range(math.floor(house_x - house_width / 2), math.ceil(house_x + house_width / 2) + 1):
                for j in range(math.floor(house_y - house_height / 2), math.ceil(house_y + house_height / 2) + 1):
                    house_points.append((i, j))
                    if self.is_occupied(i, j):
                        not_occupied_house_coord = False
            if not_occupied_house_coord:
                self.bulk_mark_as_occupied(house_points)
                house_coord_search_done = True

        self.add_item(House(pos=(house_x, house_y), height=house_height, width=house_width))

    def add_trees(self, field_type):
        """
        Add trees to a block. Need check for coord is occupied or not before adding.
        Quantity of trees differ while in a park or a yard.
        :param field_type:
        :return:
        """
        quantity_of_trees = 0
        if field_type == 'park':
            quantity_of_trees = random.randint(70, 80)
        elif field_type == 'yard':
            quantity_of_trees = random.randint(5, 10)
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
        """
        Generate rgb image of a block
        :return: rgb grid in a block
        """
        bg_rgb_colour = get_rgb_colour(self.block_bg_color)
        rgb_grid = np.ones((self.size, self.size, 3), dtype=np.uint8) * bg_rgb_colour  # 3D RGB grid, preset bg colour

        for item in self.items:
            topleft = item.get_topleft()  # topleft coord of item within Block
            img = item.get_image()  # 3D RGB image
            cx_start = max(0, int(topleft[0]))  # x is columns
            ry_start = max(0, int(topleft[1]))  # y is rows
            cx_stop = min(self.size, int(cx_start + img.shape[1]))
            ry_stop = min(self.size, int(ry_start + img.shape[0]))

            img_height = ry_stop - ry_start
            img_width = cx_stop - cx_start

            # print(f"Topleft: {topleft}, img shape: {img.shape}, grid shape: {rgb_grid.shape}")
            # print(f"Placing image from ({ry_start}:{ry_stop}, {cx_start}:{cx_stop})")

            if img_height > 0 and img_width > 0:
                # overlay item on grid
                rgb_grid[ry_start:ry_stop, cx_start:cx_stop, :] = img[:img_height, :img_width, :]
            # else:
            # print(f"Invalid slice: start ({cx_start}, {ry_start}), stop ({cx_stop}, {ry_stop})")

        return rgb_grid

    def generate_thermal_image(self, env_temperature):
        """
        Generate thermal image of a block
        :param env_temperature:
        :return: thermal_grid for a block, average temperature in this block (based on all items)
        """
        thermal_grid = np.full((self.size, self.size), 15, dtype=np.float32)  # 2d grid
        avg_temp = []
        for item in self.items:
            topleft = item.get_topleft()
            item_temp = item.get_updated_temperature(env_temperature)

            cx_start = max(0, int(topleft[0]))
            ry_start = max(0, int(topleft[1]))
            cx_stop = min(self.size, int(cx_start + item.get_width()))
            ry_stop = min(self.size, int(ry_start + item.get_height()))

            thermal_grid[ry_start:ry_stop, cx_start:cx_stop] = item_temp
            avg_temp = self.calc_avg_temp()

        # print(f"Thermal grid type: {type(thermal_grid)}, shape: {thermal_grid.shape}")

        return thermal_grid, avg_temp

    def calc_avg_temp(self):
        """
        Calculate the average temperature of items.
        :return:
        """
        mass_total = 0
        weighted_temp_total = 0

        for item in self.items:
            mass_total += item.mass
            weighted_temp_total += item.item_temperature * item.mass

        if mass_total != 0:
            return weighted_temp_total / mass_total
        else:
            return 0

    def __str__(self):
        return f"Block: {self.topleft}, #items = {len(self.items)}"


class Map:
    def __init__(self, blocks, map_config, temperature_daytime_list):
        self.blocks = blocks

        # map structure properties
        self.block_size = map_config['block_size']
        self.block_row_num = map_config['block_row_num']
        self.block_col_num = map_config['block_col_num']
        self.block_num = map_config['block_num']
        self.map_shape = map_config['map_shape']
        self.park_limit = map_config['park_limit']

        # thermal: daytime temperature list over 24 hours
        self.temperature_daytime_list = temperature_daytime_list

    def generate_map_structure(self):
        """
        generate blocks with park or yard field type based on park_limit
        rgb and thermal view share the same map structure
        :return:
        """
        field_type_choices = ['park'] * self.park_limit + ['yard'] * (self.block_num - self.park_limit)
        random.shuffle(field_type_choices)
        for i in range(self.block_row_num):
            for j in range(self.block_col_num):
                field = field_type_choices.pop()
                self.blocks.append(Block(self.block_size, ((j * self.block_size), (i * self.block_size)), field))

    def generate_rgb_view(self, blocks):
        """
        Generate rgb view for all blocks.
        :param blocks:
        :return: rgb view of the map
        """
        map_image = np.zeros((self.map_shape[0] * self.block_size, self.map_shape[1] * self.block_size, 3),
                             dtype=np.uint8)
        for block in blocks:
            block_img = block.generate_block_image()
            topleft = block.get_topleft()

            x_start, y_start = topleft
            x_end = x_start + block_img.shape[1]
            y_end = y_start + block_img.shape[0]
            map_image[y_start:y_end, x_start:x_end, :] = block_img
        return map_image

    def generate_thermal_view(self, env_temperature):
        """
            Generate thermal view for all blocks.
            :param env_temperature:
            :return: thermal view of the map
        """
        thermal_image = np.zeros((self.map_shape[0] * self.block_size, self.map_shape[1] * self.block_size),
                                 dtype=np.float32)
        avg_temps = []
        topleft_locs = []

        for block in self.blocks:
            block_img, avg_temp = block.generate_thermal_image(env_temperature)
            topleft = block.get_topleft()

            x_start, y_start = topleft
            x_end = x_start + block_img.shape[1]
            y_end = y_start + block_img.shape[0]
            thermal_image[y_start:y_end, x_start:x_end] = block_img

            avg_temps.append(avg_temp)
            topleft_locs.append(block.topleft)

        # print(f"Final thermal_image shape: {thermal_image.shape}")

        return thermal_image, avg_temps, topleft_locs