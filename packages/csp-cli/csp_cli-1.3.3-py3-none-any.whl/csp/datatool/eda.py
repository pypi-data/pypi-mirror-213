#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/9/26 17:15
# @Author  : xgy
# @Site    : 
# @File    : eda.py
# @Software: PyCharm
# @python version: 3.7.4
"""


def det_voc(dataset, output):
    """
    目标检测任务VOC数据集统计分析命令
    Parameters
    ----------
    dataset : 数据集目录
    output : 统计分析结果保存目录

    Returns
    -------

    """
    from csp.datatool.image_detection.eda import det_eda
    try:
        det_eda(dataset, form="voc", output=output)
    except Exception as ae:
        print(ae)


def det_coco(dataset, output):
    """
    目标检测任务COCO数据集统计分析命令
    Parameters
    ----------
    dataset : 数据集目录
    output : 统计分析结果保存目录

    Returns
    -------

    """
    from csp.datatool.image_detection.eda import det_eda
    try:
        det_eda(dataset, form="coco", output=output)
    except Exception as ae:
        print(ae)


def img_cls(dataset, output):
    """
    图像分类任务平台数据集统计分析命令
    Parameters
    ----------
    dataset : 数据集目录
    output : 统计分析结果保存目录

    Returns
    -------

    """
    from csp.datatool.image_classify.eda import img_classify_eda
    try:
        img_classify_eda(dataset, output=output)
    except Exception as ae:
        print(ae)


def text_entity(dataset, output):
    """
    文本实体抽取分类任务平台数据集统计分析命令
    Parameters
    ----------
    dataset : 数据集目录
    output : 统计分析结果保存目录

    Returns
    -------

    """
    from csp.datatool.text_entity.eda import entity_eda
    try:
        entity_eda(dataset, output)
    except Exception as ae:
        print(ae)


def text_entity_relation(dataset, output):
    """
    文本实体关系抽取任务平台数据集统计分析命令
    Parameters
    ----------
    dataset : 数据集目录
    output : 统计分析结果保存目录

    Returns
    -------

    """
    # 新版1json
    # from csp.datatool.text_entity_relation.eda import spo_eda
    # 旧版5json
    from csp.datatool.text_entity_relation.eda_bak import spo_eda
    try:
        spo_eda(dataset, output)
    except Exception as ae:
        print(ae)


def text_cls(dataset, output):
    """
    文本分类任务平台数据集统计分析命令
    Parameters
    ----------
    dataset : 数据集目录
    output : 统计分析结果保存目录

    Returns
    -------

    """
    from csp.datatool.text_classify.eda import text_classify_eda
    try:
        text_classify_eda(dataset, output)
    except Exception as ae:
        print(ae)


if __name__ == '__main__':
    print("start")
