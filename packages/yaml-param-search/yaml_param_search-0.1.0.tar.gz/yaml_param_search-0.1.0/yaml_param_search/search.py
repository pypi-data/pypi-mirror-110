import os
from typing import List

import yaml
import numpy as np
import copy
from yaml import Loader

"""
该参数搜索先将字典展平后计算list个数，只计算作为字典value的list而不深入计算list中的list。
统计完list个数和长度后，将长度相乘得到需要搜索的参数组合数量。
将list长度按出现顺序排列，将其作为进位标识符，表示每个位都具有不同的base，进位不同。
搜索所有参数只要把参数组合数量转换为自定义进制的数即可。该转换过程从零开始依次加一至所需的的参数数量值，依次进位，每个位即是改取的参数的位置。所以能保证搜索到所有参数。
将展平后的list与原始字典对应则直接使用self-called（刚编的名字） 函数，依次将参数传入对应。
"""


def read_yaml(name, root_path):
    with open(os.path.join(root_path, "config", name), "r") as f:
        config = yaml.load(f, Loader=Loader)
    return config


def calculate_number_of_runs(config) -> int:
    if type(config) == list:
        return len(config)
    else:
        nums = [calculate_number_of_runs(value) for key, value in config.items()]
        return np.prod(nums)


def flatten_config_and_calculate_base(config) -> List[int]:
    if type(config) == list:
        return [len(config), ]
    else:
        nums = [flatten_config_and_calculate_base(value) for key, value in config.items()]
        results = []
        for i in nums:
            results += i
        return results


def output_number_for_the_given_base(num, base: List[int]):
    def calculate_carry(number_of_base, given_base):
        assert len(number_of_base) == len(given_base)
        for i in range(len(number_of_base)):
            if number_of_base[i] == given_base[i]:
                number_of_base[i] = 0
                number_of_base[i + 1] += 1
        return number_of_base

    result = [0 for i in range(len(base))]
    for i in range(num):
        result[0] += 1
        result = calculate_carry(result, base)

    return result


def create_param_from_custom_base_numbers(number: List[int], config: dict or list):
    if type(config) == list:
        index = number.pop(0)
        return config[index]
    else:
        for key, value in config.items():
            config[key] = create_param_from_custom_base_numbers(number, config[key])
        return config


def create_param_from_config(config_name, root_path):
    """
    read yaml and
    :param root_path:
    :param config_name:
    :return:
    """
    config = read_yaml(config_name, root_path)
    custom_base = flatten_config_and_calculate_base(config)
    num_of_runs = calculate_number_of_runs(config)
    for i in range(num_of_runs):
        number_of_custom_base = output_number_for_the_given_base(i, custom_base)
        yield create_param_from_custom_base_numbers(number_of_custom_base, copy.deepcopy(config))


def save_results(text, config_name, root_path):
    if not os.path.exists(os.path.join(root_path, "logs")):
        os.mkdir(os.path.join(root_path, "logs"))
    with open(os.path.join(root_path, "logs", config_name + ".txt"), "a") as f:
        f.write(str(text))
        f.write("\n|||\n")


class Config:
    def __init__(self, path, config_name):
        self.config_name = config_name
        self.path = path

    def yield_param(self):
        return create_param_from_config(self.config_name, self.path)

    def write_logs(self, text):
        save_results(text, self.config_name, self.path)
        return self
