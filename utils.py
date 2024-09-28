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


def generate_image(blocks, block_size, map_shape):
    map_image = np.zeros((map_shape[0] * block_size, map_shape[1] * block_size, 3), dtype=np.uint8)
    for block in blocks:
        block_img = block.generate_image()
        topleft = block.get_topleft()

        x_start, y_start = topleft
        x_end = x_start + block_img.shape[1]
        y_end = y_start + block_img.shape[0]
        map_image[y_start:y_end, x_start:x_end, :] = block_img
    return map_image


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
