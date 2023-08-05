# -*- coding:utf-8 -*-
# Author:  zhousf
# Description: 目标检测bbox计算工具
# pip install matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def show_rect(boxes: list):
    """
    显示box
    :param boxes: [(x_min, y_min, x_max, y_max)]
    :return:
    [(317,280,553,395), (374,295,485,322)]
    """
    colors = list(mcolors.TABLEAU_COLORS.keys())
    plt.xlabel("x", fontweight='bold', size=14)
    plt.ylabel("y", fontweight='bold', size=14)
    ax = plt.gca()  # 坐标系
    x_max = 0
    y_max = 0
    for index, box in enumerate(boxes):
        x_max = box[2] if box[2] > x_max else x_max
        y_max = box[3] if box[3] > y_max else y_max
        ax.add_patch(
            plt.Rectangle(xy=(box[0], box[1]), width=(box[2] - box[0]), height=(box[3] - box[1]),
                          alpha=1,
                          fill=False,
                          color=colors[index],
                          facecolor=colors[index],
                          linewidth=1))
    plt.xlim(0, int(2 * x_max))
    plt.ylim(0, int(2 * y_max))
    # 转成屏幕坐标系（左上角为原点）
    ax.xaxis.set_ticks_position('top')  # 将X坐标轴移到上面
    ax.invert_yaxis()  # 反转Y坐标轴
    plt.show()


def compute_iou(predicted_box, ground_truth_box):
    """
    计算交并比
    :param predicted_box: 预测box=(x_min, y_min, x_max, y_max)
    :param ground_truth_box: 真实box=(x_min, y_min, x_max, y_max)
    :return:
    """
    px_min, py_min, px_max, py_max = predicted_box
    gx_min, gy_min, gx_max, gy_max = ground_truth_box
    p_area = (px_max - px_min) * (py_max - py_min)  # 计算P的面积
    g_area = (gx_max - gx_min) * (gy_max - gy_min)  # 计算G的面积
    # 求相交矩形的左下和右上顶点坐标(x_min, y_min, x_max, y_max)
    _x_min = max(px_min, gx_min)  # 得到左下顶点的横坐标
    _y_min = max(py_min, gy_min)  # 得到左下顶点的纵坐标
    _x_max = min(px_max, gx_max)  # 得到右上顶点的横坐标
    _y_max = min(py_max, gy_max)  # 得到右上顶点的纵坐标
    # 计算相交矩形的面积
    w = _x_max - _x_min
    h = _y_max - _y_min
    if w <= 0 or h <= 0:
        return 0
    area = w * h  # G∩P的面积
    return area / (p_area + g_area - area)


def compute_contain(box1, box2):
    """
    计算两个box是否为包含关系
    :param box1: (x_min, y_min, x_max, y_max)
    :param box2: (x_min, y_min, x_max, y_max)
    :return: 返回两个box重叠面积占较小box的面积比，一般大于0.8则为包含关系
    box1=(317,280,553,395)
    box2=(374,295,485,322)
    """
    px_min = min(box1[0], box1[2])
    py_min = min(box1[1], box1[3])
    px_max = max(box1[0], box1[2])
    py_max = max(box1[1], box1[3])
    # px_min, py_min, px_max, py_max = box1
    # gx_min, gy_min, gx_max, gy_max = box2
    gx_min = min(box2[0], box2[2])
    gy_min = min(box2[1], box2[3])
    gx_max = max(box2[0], box2[2])
    gy_max = max(box2[1], box2[3])
    p_area = (px_max - px_min) * (py_max - py_min)  # 计算P的面积
    g_area = (gx_max - gx_min) * (gy_max - gy_min)  # 计算G的面积
    # 求相交矩形的左下和右上顶点坐标(x_min, y_min, x_max, y_max)
    _x_min = max(px_min, gx_min)  # 得到左下顶点的横坐标
    _y_min = max(py_min, gy_min)  # 得到左下顶点的纵坐标
    _x_max = min(px_max, gx_max)  # 得到右上顶点的横坐标
    _y_max = min(py_max, gy_max)  # 得到右上顶点的纵坐标
    # 计算相交矩形的面积
    w = _x_max - _x_min
    h = _y_max - _y_min
    if w <= 0 or h <= 0:
        return 0
    area = w * h  # G∩P的面积
    if p_area >= g_area:
        return area / g_area
    else:
        return area / p_area


def group_by_box_overlap(od_result: list, return_area=False):
    """
    根据box的重叠面积进行分组-通用算法，适用目标检测、画图等
    :param od_result: [(?, ?, x_min, y_min, x_max, y_max)], box置于tuple最后
    :param return_area: 是否返回面积
    :return:
    [[(index, [area, (?, ?, x_min, y_min, x_max, y_max)])]]
    or
    [[(?, ?, x_min, y_min, x_max, y_max)]]
    """
    boxes = {}
    # 按照面积从大到小排序, box置于tuple最后
    for index, item in enumerate(od_result):
        (x_min, y_min, x_max, y_max) = item[-4:]
        area = (x_max - x_min) * (y_max - y_min)
        boxes[index] = [area, item]
    boxes = sorted(boxes.items(), key=lambda d: d[1], reverse=True)
    box_group = []
    has_add_index = []
    for item1 in boxes:
        (index1, [area1, box1]) = item1
        (x_min1, y_min1, x_max1, y_max1) = box1[-4:]
        items = [item1] if return_area else [box1]
        if index1 in has_add_index:
            continue
        has_add_index.append(index1)
        for i, item2 in enumerate(boxes):
            (index2, [area2, box2]) = item2
            (x_min2, y_min2, x_max2, y_max2) = box2[-4:]
            if compute_contain((x_min1, y_min1, x_max1, y_max1),
                               (x_min2, y_min2, x_max2, y_max2)) > 0.8:
                if item1 == item2:
                    continue
                if index2 in has_add_index:
                    continue
                has_add_index.append(index2)
                if return_area:
                    items.append(item2)
                else:
                    items.append(box2)
        box_group.append(items)
    return box_group


def search_right_box(boxes: list):
    """
    搜索最右侧box
    :param boxes: [(?, ?, x_min, y_min, x_max, y_max)]
    :return: box
    """
    if len(boxes) == 0:
        return None
    boxes.sort(key=lambda x: x[-2], reverse=True)
    return boxes[0]


def search_top_box(boxes: list):
    """
    搜索最顶端box
    :param boxes: [(?, ?, x_min, y_min, x_max, y_max)]
    :return: box
    """
    if len(boxes) == 0:
        return None
    boxes.sort(key=lambda x: x[-3], reverse=False)
    return boxes[0]


def search_bottom_box(boxes: list):
    """
    搜索最底端box
    :param boxes: [(?, ?, x_min, y_min, x_max, y_max)]
    :return: box
    """
    if len(boxes) == 0:
        return None
    boxes.sort(key=lambda x: x[-1], reverse=True)
    return boxes[0]


def search_nearby_bottom_box(target_box, boxes: list):
    """
    搜索紧邻target_box底部的box
    :param target_box: (?, ?, x_min, y_min, x_max, y_max)
    :param boxes: [(?, ?, x_min, y_min, x_max, y_max)]
    :return: box
    """
    if len(boxes) == 0:
        return None
    t_x = (target_box[-2] + target_box[-4]) / 2
    t_y = (target_box[-3] + target_box[-1]) / 2
    t_width = abs(target_box[-2] - target_box[-4])
    t_height = abs(target_box[-3] - target_box[-1])
    for box in boxes:
        c_x = (box[-2] + box[-4]) / 2
        c_y = (box[-3] + box[-1]) / 2
        c_width = abs(box[-2] - box[-4])
        c_height = abs(box[-3] - box[-1])
        # 两个中心点的X轴坐标差不超过两个box的高度和的一半，表示两个box在同一垂直线上
        if abs(c_x-t_x) < (t_width + c_width) / 2:
            if t_y < c_y:
                return box
    return None


def search_nearby_right_box(target_box, boxes: list):
    """
    搜索紧邻target_box右侧的box
    :param target_box: (?, ?, x_min, y_min, x_max, y_max)
    :param boxes: [(?, ?, x_min, y_min, x_max, y_max)]
    :return: box
    """
    if len(boxes) == 0:
        return None
    t_x = (target_box[-2] + target_box[-4]) / 2
    t_y = (target_box[-3] + target_box[-1]) / 2
    t_width = abs(target_box[-2] - target_box[-4])
    t_height = abs(target_box[-3] - target_box[-1])
    for box in boxes:
        c_x = (box[-2] + box[-4]) / 2
        c_y = (box[-3] + box[-1]) / 2
        c_width = abs(box[-2] - box[-4])
        c_height = abs(box[-3] - box[-1])
        # 两个中心点的Y轴坐标差不超过两个box的高度和的一半，表示两个box在同一水平线上
        if abs(c_y-t_y) < (t_height + c_height) / 2:
            if t_x < c_x:
                return box
    return None


def search_nearby_left_box(target_box, boxes: list):
    """
    搜索紧邻target_box左侧的box
    :param target_box: (?, ?, x_min, y_min, x_max, y_max)
    :param boxes: [(?, ?, x_min, y_min, x_max, y_max)]
    :return: box
    """
    if len(boxes) == 0:
        return None
    t_x = (target_box[-2] + target_box[-4]) / 2
    t_y = (target_box[-3] + target_box[-1]) / 2
    t_width = abs(target_box[-2] - target_box[-4])
    t_height = abs(target_box[-3] - target_box[-1])
    for box in boxes:
        c_x = (box[-2] + box[-4]) / 2
        c_y = (box[-3] + box[-1]) / 2
        c_width = abs(box[-2] - box[-4])
        c_height = abs(box[-3] - box[-1])
        # 两个中心点的Y轴坐标差不超过两个box的高度和的一半，表示两个box在同一水平线上
        if abs(c_y-t_y) < (t_height + c_height) / 2:
            if t_x > c_x:
                return box
    return None


def box_scale_up(box, offset=50):
    """
    box增大
    :param box:
    :param offset:
    :return:
    """
    x_min, y_min, x_max, y_max = box
    _x_min = x_min - offset
    _x_min = 0 if _x_min < 0 else _x_min
    _x_max = x_max + offset
    _y_min = y_min - offset
    _y_min = 0 if _y_min < 0 else _y_min
    _y_max = y_max + offset
    return _x_min, _y_min, _x_max, _y_max


def box_scale_down(box, offset=50):
    """
    box缩小
    :param box:
    :param offset:
    :return:
    """
    x_min, y_min, x_max, y_max = box
    offset = min(x_min, y_min) if min(x_min, y_min) < offset else offset
    _x_min = x_min + offset
    _x_max = x_max - offset
    _y_min = y_min + offset
    _y_max = y_max - offset
    return _x_min, _y_min, _x_max, _y_max


if __name__ == "__main__":
    # print(box_scale_down((10, 10, 20, 20), offset=2))
    print(box_scale_up((-166.68197631835938, -0.008893102407455444, 1810.6822509765625, 143.40452575683594), offset=2))
    # a =(168.9995880126953, 40.77224349975586, 186.8643341064453, 62.222076416015625)
    # b =(151.0, 34.0, 234.0, 77.0)
    # print(compute_iou(a, b))
    # print(compute_contain(a, b))
    # show_rect([a, b])
    # od_result = [('引线', 0.9127930998802185, 317.42401123046875, 280.783203125, 553.0108032226562,
    #               395.31756591796875), (
    #              '引线', 0.9017542600631714, 356.3954772949219, 434.4830322265625, 595.97314453125,
    #              548.5955200195312), (
    #              '普通钢筋大样图', 0.7828382253646851, 234.65667724609375, 433.5041809082031,
    #              609.3646240234375, 576.8939208984375), (
    #              '普通钢筋大样图', 0.7160109281539917, 222.05714416503906, 276.25738525390625,
    #              662.2127685546875, 420.0615539550781), (
    #              '编号', 0.7344087958335876, 505.61639404296875, 439.4078674316406, 590.3804931640625,
    #              524.0474243164062), (
    #              '编号', 0.6869884729385376, 468.19793701171875, 285.3776550292969, 550.497802734375,
    #              370.9029541015625)]
    # ocr_data = [{'bbox': [[374, 295], [486, 296], [485, 322], [373, 321]], 'label': '192史12',
    #              'confidence': 96},
    #             {'bbox': [[494, 305], [525, 305], [525, 344], [494, 344]], 'label': '1',
    #              'confidence': 95},
    #             {'bbox': [[415, 329], [459, 329], [459, 362], [415, 362]], 'label': '56',
    #              'confidence': 99},
    #             {'bbox': [[421, 357], [463, 357], [463, 389], [421, 389]], 'label': '56',
    #              'confidence': 99},
    #             {'bbox': [[422, 445], [519, 445], [519, 473], [422, 473]], 'label': '6412',
    #              'confidence': 99},
    #             {'bbox': [[536, 466], [560, 466], [560, 496], [536, 496]], 'label': '2',
    #              'confidence': 99},
    #             {'bbox': [[453, 484], [491, 484], [491, 511], [453, 511]], 'label': '50',
    #              'confidence': 99},
    #             {'bbox': [[411, 512], [450, 512], [450, 543], [411, 543]], 'label': '50',
    #              'confidence': 99}]
    # ocr_result = []
    # for data in ocr_data:
    #     box = data.get("bbox")
    #     _label = data.get("label")
    #     _score = data.get("confidence") / 100
    #     ocr_result.append((_label, _score, box[0][0], box[0][1], box[2][0], box[2][1]))
    # od_result.extend(ocr_result)
    # box_group = group_by_box_overlap(od_result)
    # for group in box_group:
    #     for item in group:
    #         (index1, [area1, box1]) = item
    #         print(item)
    #     print("---------")
    pass
