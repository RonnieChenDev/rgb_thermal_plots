import random
import numpy as np
import matplotlib.pyplot as plt
from canopy import *
from utils import *
matplotlib.use('Qt5Agg')


def main():
    # read from config file for the number of block rows, number of block columns, block size
    map_config = read_from_csv("config/map_configuration.csv")[0]
    block_size = int(map_config[2])
    block_row_num = int(map_config[0])
    block_col_num = int(map_config[1])
    block_num = block_row_num * block_col_num
    map_shape = (block_row_num, block_col_num)
    # total of blocks * percentage of park area
    park_limit = round(float(map_config[3]) * block_num)

    # create a list to hold all the blocks
    blocks = []

    # Add blocks based on configuration
    # generate blocks with park or yard field type based on park_limit
    field_type_choices = ['park'] * park_limit + ['yard'] * (block_num - park_limit)
    random.shuffle(field_type_choices)
    for i in range(block_row_num):
        for j in range(block_col_num):
            blocks.append(Block(block_size, ((j * block_size), (i * block_size)), field_type_choices.pop()))

    # Add items to blocks
    for block in blocks:
        if block.field_type == 'park':
            # if it is park, add roads and more trees
            block.add_road()
        else:
            # if it is yard, add roads, house and a few trees
            block.add_road()
            block.add_house(6, 4)

    # Top row. One house and three trees in each block.
    # blocks[0].add_item(Tree((2, 4)))
    # blocks[0].add_item(Tree((4, 15)))
    # blocks[0].add_item(Tree((12, 6)))
    # blocks[0].add_item(House((11, 12)))
    #
    # blocks[1].add_item(Tree((2, 4)))
    # blocks[1].add_item(Tree((4, 15)))
    # blocks[1].add_item(Tree((12, 6)))
    # blocks[1].add_item(House((11, 12)))
    #
    # blocks[2].add_item(Tree((2, 4)))
    # blocks[2].add_item(Tree((4, 15)))
    # blocks[2].add_item(Tree((12, 6)))
    # blocks[2].add_item(House((11, 12)))

    # Bottom row. Random trees in a range of shapes of green.
    # for _ in range(6):
    #     blocks[3].add_item(Tree((random.randint(2, 18), random.randint(2, 18))))
    #     blocks[4].add_item(Tree((random.randint(2, 18), random.randint(2, 18))))
    #     blocks[5].add_item(Tree((random.randint(2, 18), random.randint(2, 18))))

    plt.imshow(generate_image(blocks, block_size, map_shape))

    plt.title("Task 4: (2,3) grid of blocks with houses and trees")
    plt.show()


if __name__ == "__main__":
    main()
