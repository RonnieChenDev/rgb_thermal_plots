import random
import numpy as np
import matplotlib.pyplot as plt
from canopy import *
from utils import *

matplotlib.use('Qt5Agg')


def main():
    # TODO: test code

    # get map config
    map_config = get_map_config(read_from_csv("config/map_configuration.csv"))
    temperature_daytime = get_temperature_daytime(read_from_csv("config/temperature_daytime.csv"))

    # create a list to hold all the blocks
    blocks = []
    plots_map = Map(blocks, map_config, temperature_daytime)

    plots_map.generate_map_structure()

    # Start to add rgb blocks based on configuration
    # Add items to blocks in the sequence of road, house (if on field_type 'yard') and trees.
    for block in blocks:
        if block.field_type == 'park':
            # if it is park, add roads and more trees
            block.add_road(1, 1)
            block.add_trees(block.field_type)
        else:
            # if it is yard, add roads, house and a few trees
            block.add_road(2, 2)
            block.add_house(4, 6)
            block.add_trees(block.field_type)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

    ax1.imshow(plots_map.generate_rgb_view(blocks))
    ax1.set_title("RGB view")

    # initial
    thermal_view, avg_temps, topleft_locs = plots_map.generate_thermal_view(temperature_daytime[0])
    cax = ax2.imshow(thermal_view, cmap='hot', vmin=10, vmax=50)
    ax2.set_title(f"Thermal View at {temperature_daytime[0]}")
    fig.colorbar(cax, ax=ax2, shrink=0.6)

    for hour, temp in enumerate(temperature_daytime):
        thermal_view, avg_temps, topleft_locs = plots_map.generate_thermal_view(temp)
        cax.set_data(thermal_view)
        if hour < 16:
            current_hour = hour + 8
        else:
            current_hour = hour + 8 - 24

        ax2.set_title(f"Thermal View at {temp} °C, time at hour {current_hour}")

        # clear the text if any
        for txt in ax2.texts:
            txt.remove()
        # avg temperature print
        for index, temp in enumerate(avg_temps):
            x, y = topleft_locs[index]
            # move text a little downwards
            ax2.text(x, (y + 1), f'{temp:.1f}', color='white')

        plt.pause(1)

    plt.show()


if __name__ == "__main__":
    main()
