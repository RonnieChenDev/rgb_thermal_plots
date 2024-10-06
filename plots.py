import matplotlib.pyplot as plt
from canopy import *
from utils import *
import time

matplotlib.use('Qt5Agg')


def main():
    map_config_list = []

    # Prompt to ask which scenario to simulate with, and require manual input or not.
    # Keep doing the while loop to do the simulation until get system input for quit.
    print("Welcome to the thermal simulation system! \n")
    print("Would you like to do the simulation?")
    user_selected_system_action = -1
    system_options = ['Start simulation', 'Quit']
    user_selected_system_action = option_list_loop(user_selected_system_action, system_options)

    while user_selected_system_action == 0:
        print("\nPlease select a scenario to simulate with:")
        scenario_options = ['High fixed temperature', 'Low fixed temperature', 'Continuously changing temperature']
        user_selected_scenario = -1
        user_selected_scenario = option_list_loop(user_selected_scenario, scenario_options)

        print("\nThank you! Now some information of map is required from you.")
        print("Would you like to input by yourself or using the content in config and temperature file?")
        user_selected_input_mode = -1
        input_modes = ['Input by myself', 'Use files directly']
        user_selected_input_mode = option_list_loop(user_selected_input_mode, input_modes)

        if user_selected_input_mode == 0:
            print("\nPlease enter map config.")
            # assume user's input is float numbers. Simply decide on length of input.
            while len(map_config_list) != 4:
                map_input = input("Sequence is quantity of block rows, quantity of block columns, block size and "
                                  "park percentage, separating with ',':")
                map_config_list = map_input.split(',')
                if len(map_config_list) != 4:
                    print("Invalid quantity of params, please re-enter! \n")

            map_config_list = [float(i) for i in map_config_list]
            # keys = ['block_size', 'block_row_num', 'block_col_num', 'block_num', 'map_shape', 'park_limit']
            # park limit need transform from percentage to a fixed quantity
            block_num = int(map_config_list[0]) * int(map_config_list[1])
            map_shape = (int(map_config_list[0]), int(map_config_list[1]))
            park_limit = round(float(map_config_list[3]) * block_num)

            map_config = {"block_size": int(map_config_list[2]), "block_row_num": int(map_config_list[0]),
                          "block_col_num": int(map_config_list[1]), "block_num": block_num,
                          "map_shape": map_shape, "park_limit": park_limit}

            print("\nThank you! Then do you want to input the temperature to simulate with on your own? \n")
            temperature_option = input("Please type in y or n:")
            if temperature_option.lower() == 'y':
                if user_selected_scenario == 0 or user_selected_scenario == 1:
                    env_temp_for_generate_list = float(input("\nPlease enter the temperature using integer "
                                                             "between 0 and 45: "))
                    env_temp = [env_temp_for_generate_list] * 24
                else:
                    env_temp_string = input("\nPlease enter the temperature using integer between 0 and 45, "
                                            "split with ',': ")
                    env_temp = env_temp_string.split(',')
            else:
                env_temp = get_temperature_daytime(read_from_csv("config/temperature_daytime.csv"),
                                                   user_selected_scenario)
        else:
            map_config = get_map_config(read_from_csv("config/map_configuration.csv"))
            env_temp = get_temperature_daytime(read_from_csv("config/temperature_daytime.csv"), user_selected_scenario)

        # create a list to hold all the blocks
        blocks = []
        plots_map = Map(blocks, map_config, env_temp)

        plots_map.generate_map_structure()

        # Start to add rgb blocks based on configuration
        # Add items to blocks in the sequence of road, house (if on field_type 'yard') and trees.
        for block in blocks:
            if block.field_type == 'park':
                # if it is park, add roads and more trees
                block.add_road(1, 1)
                block.add_trees(block.field_type)
            else:
                # if it is yard, randomly add roads, house and a few trees.
                block.add_road(2, 2)
                block.add_house(4, 6)
                block.add_trees(block.field_type)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

        ax1.imshow(plots_map.generate_rgb_view(blocks))
        ax1.set_title("RGB view")

        # initial
        thermal_view, avg_temps, topleft_locs = plots_map.generate_thermal_view(env_temp[0])
        cax = ax2.imshow(thermal_view, cmap='hot', vmin=0, vmax=50)
        ax2.set_title(f"Thermal View at {env_temp[0]}")
        fig.colorbar(cax, ax=ax2, shrink=0.6)

        for hour, temp in enumerate(env_temp):
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
            for index, avg_temp in enumerate(avg_temps):
                x, y = topleft_locs[index]
                # move text a little downwards
                ax2.text(x, (y + 1), f'{avg_temp:.1f}', color='white')

            plt.pause(1)

        plt.show()

        # ask for the system option again
        next_user_selected_system_action = -1
        next_user_selected_system_action = option_list_loop(next_user_selected_system_action, system_options)
        if next_user_selected_system_action == 1:
            print("\nThank you for using the system, bye!")
            user_selected_system_action = 1


if __name__ == "__main__":
    main()
