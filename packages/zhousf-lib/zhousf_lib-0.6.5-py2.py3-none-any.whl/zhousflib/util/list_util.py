# -*- coding:utf-8 -*-
# Author:  zhousf
# Description:


def none_filter(data: list):
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

