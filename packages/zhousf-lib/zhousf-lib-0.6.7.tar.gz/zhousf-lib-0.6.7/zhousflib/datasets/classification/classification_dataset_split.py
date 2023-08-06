# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Function: 图像分类数据制作
import shutil
import imghdr
import numpy as np
from pathlib import Path


def fetch_available_cls_folder(img_dir: Path):
    """
    删除空目录
    :param img_dir:
    :return:
    """
    for folder in img_dir.iterdir():
        cls = [i for i in folder.rglob("*.*")]
        if len(cls) == 0:
            print(folder)
            shutil.rmtree(folder)


def train_test_split(image_dir: Path, val_size=0.2, test_size=0.2, shuffle=True):
    """
    训练集、验证集、测试集划分
    :param image_dir: 图片目录
    :param val_size: 验证集占比
    :param test_size: 测试集占比
    :param shuffle: 打乱数据集顺序
    :return:
    """
    train_txt_file = image_dir.parent.joinpath("train_list.txt")
    val_txt_file = image_dir.parent.joinpath("val_list.txt")
    test_txt_file = image_dir.parent.joinpath("test_list.txt")
    label_list_file = image_dir.parent.joinpath("label_list.txt")
    images = []
    label_list = []
    # 标签文件
    for folder in image_dir.rglob("*.*"):
        if folder.parent.name not in label_list:
            label_list.append(folder.parent.name)
    if not label_list_file.exists():
        with label_list_file.open("w", encoding="utf-8") as f:
            for i, d in enumerate(label_list):
                f.write("{0} {1}\n".format(i, d))
    # 遍历所有图片文件
    for folder in image_dir.rglob("*.*"):
        if not folder.is_file():
            continue
        if not imghdr.what(folder):
            continue
        file = "{0}/{1}/{2} {3}\n".format(folder.parent.parent.name, folder.parent.name, folder.name, label_list.index(folder.parent.name))
        print(file)
        images.append(file)
    # 打乱顺序
    if shuffle:
        state = np.random.get_state()
        np.random.shuffle(images)
        np.random.set_state(state)
    dataset_val = []
    dataset_test = []
    split_index = 0
    if 1 > val_size > 0:
        split_index = int(len(images) * val_size)
        dataset_val = images[:split_index]
    if 1 > test_size > 0:
        start = split_index
        split_index += int(len(images) * test_size)
        dataset_test = images[start:split_index]
    dataset_train = images[split_index:]
    # 训练集
    if len(dataset_train) > 0:
        with train_txt_file.open("w", encoding="utf-8") as f:
            for d in dataset_train:
                f.write(d)
    # 验证集
    if len(dataset_val) > 0:
        with val_txt_file.open("w", encoding="utf-8") as f:
            for d in dataset_val:
                f.write(d)
    # 测试集集
    if len(dataset_test) > 0:
        with test_txt_file.open("w", encoding="utf-8") as f:
            for d in dataset_test:
                f.write(d)


if __name__ == "__main__":
    pass





