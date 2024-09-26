import numpy as np


# return the content in the file, in list. Figures are transferred from string to integer.
def read_from_csv(file_path):
    with open(file_path) as fp:
        # first line is instruction by default. Only return content starting from the second line.
        file_content = []
        for line in fp.readlines()[1:]:
            file_content.append(line.split(','))

        return file_content


def generate_image(b, s, mshape):
    grid = np.zeros((mshape[0] * s, mshape[1] * s))
    print(grid)
    for block in b:
        (cx_start, ry_start) = block.get_topleft()  # x,y mapping to column,row
        print(block, cx_start, ry_start)
        grid[ry_start:ry_start + s, cx_start:cx_start + s] = block.generate_image()[:, :]
    return grid
