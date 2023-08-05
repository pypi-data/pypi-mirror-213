#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/7/1 10:33
# @Author  : xgy
# @Site    : 
# @File    : split.py
# @Software: PyCharm
# @python version: 3.7.4
"""

# from csp.datatool.text_entity.split import entity_split as text_classify_split
from csp.datatool.utils import EntitySplitBack


def text_classify_split(folder, ratio=0.9, output=None):
    filter_entity = EntitySplitBack(folder, output=output)
    filter_entity.get_dataset()
    filter_entity.filter_by_scr(ratio=ratio)


if __name__ == '__main__':
    print("start")
