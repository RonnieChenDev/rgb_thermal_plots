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
    park_limit = round(float(map_config[3]) * block_num)
    blocks = []

    # Add blocks based on configuration.
    field_type_choices = ['park'] * park_limit + ['yard'] * (block_num - park_limit)
    random.shuffle(field_type_choices)
    for i in range(block_row_num):
        for j in range(block_col_num):
            blocks.append(Block(block_size, ((j * block_size), (i * block_size)), field_type_choices.pop()))

    # Add items to blocks.
    for block in blocks:
        if block.field_type == 'park':
            # if it is park, add roads and more trees
            ...
        else:
            # if it is yard, add roads, house and a few trees
            ...

    # Top row. One house and three trees in each block.
    blocks[0].add_item(Tree((2, 4)))
    blocks[0].add_item(Tree((4, 15)))
    blocks[0].add_item(Tree((12, 6)))
    blocks[0].add_item(House((11, 12)))

    blocks[1].add_item(Tree((2, 4)))
    blocks[1].add_item(Tree((4, 15)))
    blocks[1].add_item(Tree((12, 6)))
    blocks[1].add_item(House((11, 12)))

    blocks[2].add_item(Tree((2, 4)))
    blocks[2].add_item(Tree((4, 15)))
    blocks[2].add_item(Tree((12, 6)))
    blocks[2].add_item(House((11, 12)))

    # Bottom row. Random trees in a range of shapes of green.
    for _ in range(6):
        blocks[3].add_item(Tree((random.randint(2, 18), random.randint(2, 18))))
        blocks[4].add_item(Tree((random.randint(2, 18), random.randint(2, 18))))
        blocks[5].add_item(Tree((random.randint(2, 18), random.randint(2, 18))))

    plt.imshow(generate_image(blocks, block_size, map_shape))
    # plt.colorbar()

    # draw red grids between the blocks
    # numrows = 2
    # numcols = 3
    #
    # y_zeros = np.zeros(numcols + 1)
    # x_range = np.arange(0, numcols * 20 + 1, 20)
    # x_range[numcols] = x_range[numcols]
    # x_zeros = np.zeros(numrows + 1)
    # y_range = np.arange(0, numrows * 20 + 1, 20)
    # y_range[numrows] = y_range[numrows]
    #
    # for i in range(0, numcols * 20, 20):
    #     plt.plot(x_zeros + i, y_range - 0.5, "red", linewidth=2.5)
    # for j in range(0, numrows * 20, 20):
    #     plt.plot(x_range - 0.5, y_zeros + j, "red", linewidth=2.5)

    plt.title("Task 4: (2,3) grid of blocks with houses and trees")
    plt.show()


if __name__ == "__main__":
    main()
