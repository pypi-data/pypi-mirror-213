#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/7/1 15:49
# @Author  : xgy
# @Site    : 
# @File    : eda.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import os

from loguru import logger
import matplotlib.pyplot as plt
from csp.datatool.utils import Entity


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class SpoEda(Entity):

    def __init__(self, folder, output=None):
        super(SpoEda, self).__init__(folder, output)
        self.output = output

    def eda(self):
        self.get_dataset()
        self.eda_relation()

    def eda_relation(self):
        # self.load_relation_data()

        relation_dict_count = {}
        for item in self.data:
            spo_list = item["spo_list"]
            for spo in spo_list:
                relation = spo["relation"]
                relation_dict_count[relation] = relation_dict_count.get(relation, 0) + 1

        dpi = 15

        # 条形图
        x_index = []
        x_data = []
        y_data = []

        index = 1
        for k, v in relation_dict_count.items():
            x_data.append(k)
            y_data.append(int(v))
            x_index.append(index)
            index += 1
        plt.figure(figsize=(80, 40))
        plt.xlabel('关系', fontsize=80, loc='right')
        plt.ylabel('数量', fontsize=80)
        plt.title('关系数量分布', fontsize=100)
        plt.xticks(x_index, x_data, size=60, rotation=25)
        plt.bar(x_index, y_data, tick_label=x_data, align="center")

        for a, b in zip(x_index, y_data):
            plt.text(a, b + 0.01, b, ha='center', va='bottom', size=100)

        if self.output:
            os.makedirs(self.output, exist_ok=True)
        plt.savefig(os.path.join(self.output, 'relation_num.png'), dpi=dpi)
        logger.info("统计分析结果已保存至 {}".format(self.output))


def spo_eda(data_dir, output):

    data_eda = SpoEda(data_dir, output)
    data_eda.eda()


if __name__ == '__main__':
    print("start")
