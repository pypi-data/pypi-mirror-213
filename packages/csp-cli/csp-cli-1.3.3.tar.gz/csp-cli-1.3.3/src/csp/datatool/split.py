#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/9/26 15:22
# @Author  : xgy
# @Site    : 
# @File    : transform.py
# @Software: PyCharm
# @python version: 3.7.4
"""


def det_voc(dataset, ratio, output):
    """
    目标检测任务VOC数据集切分命令
    Parameters
    ----------
    output : 切分保存目录
    dataset : 数据集目录
    ratio : 切分后训练数据比例

    Returns
    -------

    """
    from csp.datatool.image_detection.split import det_split
    try:
        det_split(folder=dataset, form="voc", ratio=ratio, output=output)
    except Exception as ae:
        print(ae)


def det_coco(dataset, ratio, output):
    """
    目标检测任务COCO数据集切分命令
    Parameters
    ----------
    dataset : 数据集目录
    ratio : 切分后训练数据比例
    output : 切分保存目录
    # mode : 切分依据，当同时存在train.txt、trainval.txt文件时，指定其一

    Returns
    -------

    """
    from csp.datatool.image_detection.split import det_split
    try:
        det_split(folder=dataset, form="coco", ratio=ratio, output=output)
    except Exception as ae:
        print(ae)


def text_entity(dataset, ratio, output=None):
    """
    文本实体抽取任务平台格式数据集切分命令
    Parameters
    ----------
    output : 切分结果保存目录
    dataset : 数据集目录
    ratio : 切分后训练数据比例

    Returns
    -------

    """
    from csp.datatool.text_entity.split import entity_split
    try:
        entity_split(folder=dataset, ratio=ratio, output=output)
    except Exception as ae:
        print(ae)


def text_entity_relation(dataset, ratio, output=None):
    """
    文本实体关系抽取任务平台格式数据集切分命令
    Parameters
    ----------
    output : 切分保存目录
    dataset : 数据集目录
    ratio : 切分后训练数据比例

    Returns
    -------

    """
    # 旧版5json
    from csp.datatool.text_entity_relation.split_bak import spo_split
    # 新版1json
    # from csp.datatool.text_entity_relation.split import spo_split
    try:
        spo_split(folder=dataset, ratio=ratio, output=output)
    except Exception as ae:
        print(ae)


def text_cls(dataset, ratio, output):
    """
    文本分类任务平台格式数据集切分命令
    Parameters
    ----------
    dataset : 数据集目录
    ratio : 切分后训练数据比例
    output : 切分保存目录

    Returns
    -------

    """
    from csp.datatool.text_classify.split import text_classify_split
    try:
        text_classify_split(folder=dataset, ratio=ratio, output=output)
    except Exception as ae:
        print(ae)


def img_cls(dataset, ratio, output):
    """
    图像分类任务平台格式数据集切分命令
    Parameters
    ----------
    dataset : 数据集目录
    ratio : 切分后训练数据比例
    output : 切分保存目录

    Returns
    -------

    """
    from csp.datatool.image_classify.split import img_classify_split
    try:
        img_classify_split(folder=dataset, ratio=ratio, output=output)
    except Exception as ae:
        print(ae)


if __name__ == '__main__':
    print("start")
