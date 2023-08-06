# -*- coding:utf-8 -*-
# Author:  zhousf
# Description:
import imghdr
import base64
import hashlib
from pathlib import Path


def get_file_base64(file_file: Path):
    with file_file.open('rb') as infile:
        s = infile.read()
    return base64.b64encode(s).decode("utf-8")


def md5(file_path: Path):
    with file_path.open('rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def rename_image_with_md5(src_dir: Path, dst_dir: Path):
    if not dst_dir.exists():
        dst_dir.mkdir()
    count = 0
    repeat = 0
    for file in src_dir.rglob("*.*"):
        if not imghdr.what(str(file)):
            continue
        print(file.name)
        count += 1
        new_name = md5(file)
        new_name += file.suffix
        print(new_name)
        if dst_dir.joinpath(new_name).exists():
            repeat += 1
            continue
        file.rename(dst_dir.joinpath(new_name))
    print("count=", count)
    print("repeat=", repeat)


if __name__ == "__main__":
    src_dir_ = Path("/Users/zhousf/Desktop/工作空间/土建排布图/标注数据/目标检测/第3批/第三批已筛选图纸-3.24交付")
    dst_dir_ = Path("/Users/zhousf/Desktop/工作空间/土建排布图/标注数据/目标检测/第3批/原图1")
    rename_image_with_md5(src_dir_, dst_dir_)
