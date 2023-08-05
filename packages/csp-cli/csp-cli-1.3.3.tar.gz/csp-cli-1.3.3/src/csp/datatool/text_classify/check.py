#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/6/30 17:13
# @Author  : xgy
# @Site    : 
# @File    : check.py
# @Software: PyCharm
# @python version: 3.7.4
"""
from loguru import logger

# from csp.datatool.text_entity.check import EntityCheck
from csp.datatool.utils import EntityCheckBack


class TextClassifyCheck:

    """
    文本分类数据集
    """

    def __init__(self, data_dir, output):
        self.data_dir = data_dir
        self.output = output
        self.check_entity = EntityCheckBack(data_dir, output)

    def check(self):
        self.check_entity.clean_output()
        self.check_entity.get_dataset()
        # 第一步判断json文件是否能打开
        flag_json = self.check_entity.check_json()

        if flag_json:
            flag_sources = self.check_entity.check_sources()
            flag_labelcategory = self.check_entity.check_labelcategory()
            if flag_sources and flag_labelcategory:
                self.check_entity.check_labels()
            else:
                logger.warning("{} 或 {} 存在问题. {} 将不会进行错误检查".format(
                    self.check_entity.sources_path, self.check_entity.label_categories_path, self.check_entity.labels_path))


def text_classify_check(folder, output=None):
    data_check = TextClassifyCheck(folder, output)
    data_check.check()


if __name__ == '__main__':
    print("start")
