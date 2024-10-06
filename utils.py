"""
    utils.py - utils to handle files/colours/file content/prompt.

    Student Name: Xi CHEN
    Student ID  : 22278096
"""
import numpy as np


def read_from_csv(file_path):
    """
    Return the content in the file, in list. Figures are transferred from string to integer.
    First line of the file is instruction by default. Only return content starting from the second line.

    :param: file_path
    :return: file_content
    """
    try:
        with open(file_path) as fp:
            file_content = []
            for line in fp.readlines()[1:]:
                file_content.append(line.split(','))
            return file_content

    except FileNotFoundError as e:
        raise RuntimeError(f"Failed to find the target file. {e}")


def get_rgb_colour(colour_name):
    """
    Return rgb colour in the map for specific colour name.
    :param: colour_name
    :return: rgb colour, white by default
    """
    colour_map = {
        'pine_green': [1, 121, 111],
        'grey': [50, 50, 50],
        'brown': [139, 69, 19],
        'orange': [255, 165, 0],
        'pale_green': [152, 251, 152],
        'light_grey': [169, 169, 169]
    }
    return colour_map.get(colour_name, [255, 255, 255])


def get_map_config(map_config_content_list):
    """
    Convert content from map_configuration file into a map.
    :param: map_config_content_list:
    :return: map_config map
    """
    if len(map_config_content_list[0]) != 4:
        return {}
    else:
        try:
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
        except ValueError as e:
            raise ValueError(f"Values from map config file are not correct, please check! {e}")


def get_temperature_daytime(temperature_daytime_content_list, scenario_index):
    """
    Return temperature_list from temperature_daytime file for specific scenario.
    :param temperature_daytime_content_list:
    :param scenario_index:
    :return: temperature_list
    """
    if len(temperature_daytime_content_list) != 3:
        return []
    else:
        temperature_list = temperature_daytime_content_list[scenario_index]
        return temperature_list


def option_list_loop(user_selected_option, option_list):
    """
    Handle prompt input, loop until get a valid input (in terms of index of input option list)
    :param user_selected_option:
    :param option_list:
    :return: user_selected_option
    """
    for i, option in enumerate(option_list):
        print(f'{i}, {option}')

    while user_selected_option == -1:
        try:
            user_input = int(input("\nPlease enter your option:"))
            if user_input not in np.arange(len(option_list)):
                print("No such option. Please re-enter!")
            else:
                user_selected_option = user_input
        except ValueError as e:
            print("Invalid input, please re-enter!")

    return user_selected_option
