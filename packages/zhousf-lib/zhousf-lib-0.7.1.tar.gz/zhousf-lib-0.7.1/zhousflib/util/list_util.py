# -*- coding:utf-8 -*-
# Author:  zhousf
# Description:
import random


def random_choices(data_list: list, choose_k=3) -> list:
    """
    从列表中随机抽取choose_k个数（会有重复值）
    :param data_list:
    :param choose_k:
    :return:
    """
    return random.choices(data_list, k=choose_k)


def none_filter(data: list) -> list:
    """
    去掉list中的None值
    :param data:
    :return:
    """
    if isinstance(data, list):
        res = []
        for item in data:
            if isinstance(item, list):
                res.append(list(filter(None, item)))
            else:
                res = list(filter(None, data))
                break
        return res
    return data

