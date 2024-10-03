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

    plots_map.generate_map_structure()

    # Start to add rgb blocks based on configuration
    # Add items to blocks
    for block in rgb_blocks:
        if block.field_type == 'park':
            # if it is park, add roads and more trees
            block.add_road(1, 1)
            block.add_trees(block.field_type)
        else:
            # if it is yard, add roads, house and a few trees
            block.add_road(1, 1)
            block.add_house(4, 6)
            block.add_trees(block.field_type)

    plt.imshow(plots_map.generate_rgb_view(rgb_blocks))

    plt.title("Task 4: (2,3) grid of blocks with houses and trees")
    plt.show()


if __name__ == "__main__":
    main()
