#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/9/26 17:20
# @Author  : xgy
# @Site    : 
# @File    : aug.py
# @Software: PyCharm
# @python version: 3.7.4
"""


def det_voc(dataset, aug_file, mode=None):
    """
    目标检测任务VOC数据增强命令
    Parameters
    ----------
    dataset : 数据集目录，支持VOC格式
    aug_file : 增强配置yml文件
    mode : 增强依据，当同时存在train.txt、trainval.txt文件时，指定其一

    Returns
    -------

    """
    from csp.datatool.image_detection.aug import det_aug
    try:
        det_aug(dataset, aug_file, "voc", mode)
    except Exception as ae:
        print(ae)


def det_coco(dataset, aug_file, mode=None):
    """
    目标检测任务VOC数据增强命令
    Parameters
    ----------
    dataset : 数据集目录，支持coco格式
    aug_file : 增强配置yml文件
    mode : 增强依据，当同时存在train.txt、trainval.txt文件时，指定其一

    Returns
    -------

    """
    from csp.datatool.image_detection.aug import det_aug
    try:
        det_aug(dataset, aug_file, "coco", mode)
    except Exception as ae:
        print(ae)
    # det_aug(dataset, aug_file, "coco", mode)


def img_cls(dataset, aug_file):
    """
    图像分类任务平台数据增强命令
    Parameters
    ----------
    dataset : 数数据集目录，支持平台格式数据集
    aug_file : 增强配置yml文件

    Returns
    -------

    """
    from csp.datatool.image_classify.aug import img_classify_aug
    try:
        img_classify_aug(dataset, aug_file)
    except Exception as ae:
        print(ae)


if __name__ == '__main__':
    print("start")
