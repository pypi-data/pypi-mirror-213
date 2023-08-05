#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/4/26 15:58
# @Author  : xgy
# @Site    : 
# @File    : split.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import json
import os

from loguru import logger

from csp.datatool.utils import Entity, Filter


class EntitySplit(Entity):

    def __init__(self, folder, output=None):
        super(EntitySplit, self).__init__(folder, output)
        self.output = output if output else self.folder

    def filter_by_id(self, ratio=0.9):
        self.get_ids()
        size = len(self.ids)
        filter = Filter(size)
        index_train = filter.choice_random(ratio=ratio)

        train = []
        test = []
        test_id = []
        for index, item in enumerate(self.data):
            if index in index_train:
                train.append(item)
            else:
                test.append(item)
                test_id.append(item["id"])

        if self.output:
            output_train = os.path.join(self.output, "train")
            output_val = os.path.join(self.output, "eval")
        else:
            output_train = os.path.join(self.folder, "train")
            output_val = os.path.join(self.folder, "eval")

        os.makedirs(output_train, exist_ok=True)
        os.makedirs(output_val, exist_ok=True)

        labels_train_path = os.path.join(output_train, "train.json")
        labels_val_path = os.path.join(output_val, "eval.json")

        data_dict = {labels_train_path: train,
                     labels_val_path: test}

        for k, v in data_dict.items():
            with open(k, "w", encoding="utf-8") as fw:
                for item in v:
                    fw.write(json.dumps(item, ensure_ascii=False))
                    fw.write("\n")
            logger.info("切分结果已保存至 {}".format(k))

        return train, test


def entity_split(folder, ratio=0.9, output=None):
    if output:
        os.makedirs(output, exist_ok=True)
    filter_entity = EntitySplit(folder, output=output)
    filter_entity.get_dataset()
    filter_entity.filter_by_id(ratio=ratio)


if __name__ == '__main__':
    print("start")
