#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/9/26 16:30
# @Author  : xgy
# @Site    : 
# @File    : check.py
# @Software: PyCharm
# @python version: 3.7.4
"""


def det_voc(dataset, output):
    """
    目标检测任务VOC数据集检查命令
    Parameters
    ----------
    dataset : 数据集目录
    output : 检查结果保存目录

    Returns
    -------

    """
    from csp.datatool.image_detection.check import det_check
    try:
        det_check(dataset, form="voc", output=output)
    except Exception as ae:
        print(ae)


def det_coco(dataset, output):
    """
    目标检测任务COCO数据集检查命令
    Parameters
    ----------
    dataset : 数据集目录
    output : 检查结果保存目录

    Returns
    -------

    """
    from csp.datatool.image_detection.check import det_check

    try:
        det_check(dataset, form="coco", output=output)
    except Exception as ae:
        print(ae)


def text_entity(dataset, output):
    """
    文本实体抽取任务平台数据集检查命令
    Parameters
    ----------
    dataset : 数据集目录
    output : 检查结果保存目录

    Returns
    -------

    """
    from csp.datatool.text_entity.check import entity_check
    try:
        entity_check(dataset, output=output)
    except Exception as ae:
        print(ae)


def text_entity_relation(dataset, output):
    """
    文本实体关系抽取任务平台数据集检查命令
    Parameters
    ----------
    dataset : 数据集目录
    output : 检查结果保存目录

    Returns
    -------

    """
    # 新版1json
    # from csp.datatool.text_entity_relation.check import spo_check
    # 旧版5json
    from csp.datatool.text_entity_relation.check_bak import spo_check
    try:
        spo_check(dataset, output=output)
    except Exception as ae:
        print(ae)


def text_cls(dataset, output):
    """
    文本分类任务平台数据集检查命令
    Parameters
    ----------
    dataset : 数据集目录
    output : 检查结果保存目录

    Returns
    -------

    """
    from csp.datatool.text_classify.check import text_classify_check
    try:
        text_classify_check(dataset, output=output)
    except Exception as ae:
        print(ae)


def img_cls(dataset, output):
    """
    图像分类任务平台数据集检查命令
    Parameters
    ----------
    dataset : 数据集目录
    output : 检查结果保存目录

    Returns
    -------

    """
    from csp.datatool.image_classify.check import img_classify_check
    try:
        img_classify_check(dataset, output=output)
    except Exception as ae:
        print(ae)


if __name__ == '__main__':
    print("start")
