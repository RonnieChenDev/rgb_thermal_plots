import random
import numpy as np
import matplotlib.pyplot as plt
from canopy import *
from utils import *

matplotlib.use('Qt5Agg')


def main():
    # get map config
    map_config = get_map_config(read_from_csv("config/map_configuration.csv"))

    # create a list to hold all the blocks
    rgb_blocks = []
    thermal_blocks = []
    plots_map = Map(rgb_blocks, thermal_blocks, map_config)

    block_size = plots_map.block_size
    block_row_num = plots_map.block_row_num
    block_col_num = plots_map.block_col_num
    block_num = plots_map.block_num
    map_shape = plots_map.map_shape
    park_limit = plots_map.park_limit

    # Start to add rgb blocks based on configuration

    # generate blocks with park or yard field type based on park_limit
    # rgb and thermal view share the same map structure
    # field_type_choices = ['park'] * park_limit + ['yard'] * (block_num - park_limit)
    # random.shuffle(field_type_choices)
    # for i in range(block_row_num):
    #     for j in range(block_col_num):
    #         rgb_blocks.append(Block(block_size, ((j * block_size), (i * block_size)), field_type_choices.pop()))
    #         thermal_blocks.append(Block(block_size, ((j * block_size), (i * block_size)), field_type_choices.pop()))
    plots_map.generate_map_structure()

    # Add items to blocks
    for block in rgb_blocks:
        if block.field_type == 'park':
            # if it is park, add roads and more trees
            block.add_road()
            block.add_trees(block.field_type)
        else:
            # if it is yard, add roads, house and a few trees
            block.add_road()
            block.add_house(6, 4)
            block.add_trees(block.field_type)

    # plt.imshow(generate_rgb_image(rgb_blocks, block_size, map_shape))
    plt.imshow(plots_map.generate_rgb_view(rgb_blocks))

    plt.title("Task 4: (2,3) grid of blocks with houses and trees")
    plt.show()


if __name__ == "__main__":
    main()
