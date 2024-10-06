"""
    testCano.py - testing for cano.py.

    Student Name: Xi CHEN
    Student ID  : 22278096
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cano import *

print("Print objects")
block = Block(40, (0, 40), 'yard')
block.add_road(5, 5)
block.add_house(10, 5)
block.add_trees('yard')

print(block)
for item in block.items:
    print(item.pos)

block_rgb_img = block.generate_block_image()
block_thermal_img = block.generate_thermal_image(30)

print(f'block_rgb_img:\n{block_rgb_img}')
print(f'block_thermal_img:\n{block_thermal_img}')
