import numpy as np
import random
from canopy import *


# return the content in the file, in list. Figures are transferred from string to integer.
def read_from_csv(file_path):
    with open(file_path) as fp:
        # first line is instruction by default. Only return content starting from the second line.
        file_content = []
        for line in fp.readlines()[1:]:
            file_content.append(line.split(','))

        return file_content


def get_rgb_colour(colour_name):
    colour_map = {
        'pine_green': [1, 121, 111],
        'grey': [50, 50, 50],
        'brown': [139, 69, 19],
        'orange': [255, 165, 0],
        'pale_green': [152, 251, 152],
        'light_grey': [169, 169, 169]
    }
    # return white by default
    return colour_map.get(colour_name, [255, 255, 255])


def get_map_config(map_config_content_list):
    block_size = int(map_config_content_list[0][2])
    block_row_num = int(map_config_content_list[0][0])
    block_col_num = int(map_config_content_list[0][1])
    block_num = block_row_num * block_col_num
    map_shape = (block_row_num, block_col_num)

    # total of blocks * percentage of park area
    park_limit = round(float(map_config_content_list[0][3]) * block_num)

    map_config = {"block_size": block_size, "block_row_num": block_row_num, "block_col_num": block_col_num,
                  "block_num": block_num, "map_shape": map_shape, "park_limit": park_limit}

    return map_config
