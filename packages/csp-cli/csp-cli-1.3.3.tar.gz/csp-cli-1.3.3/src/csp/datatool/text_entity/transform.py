#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/10/21 10:15
# @Author  : xgy
# @Site    : 
# @File    : transform.py
# @Software: PyCharm
# @python version: 3.7.13
"""
import json
import os

from csp.common.utils import check_jsonl
from loguru import logger


def std_doccano(data_folder, output):
    st_data, file_name = check_jsonl(data_folder)
    doccano_data = []
    for item in st_data:
        id = item["id"]
        text = item["text"]
        tags = item["tags"]
        doccano_item = {"id": id, "text": text, "entities": []}
        for index, tag in enumerate(tags):
            entity = {"id": index, "label": tag["category"], "start_offset": tag["start"],
                      "end_offset": int(tag["start"]) + len(tag["mention"])}
            doccano_item["entities"].append(entity)
            doccano_item["relations"] = []
        doccano_data.append(doccano_item)

    os.makedirs(output, exist_ok=True)
    save_path = os.path.join(output, file_name)
    with open(save_path, "w", encoding="utf-8") as fw:
        for item in doccano_data:
            fw.write(json.dumps(item, ensure_ascii=False))
            fw.write("\n")
    logger.info("转换结果已保存至 {}".format(output))


def doccano_std(data_folder, output):
    doccano_data, file_name = check_jsonl(data_folder)
    st_data = []
    for item in doccano_data:
        id = item["id"]
        text = item["text"]
        entities = item["entities"]
        st_item = {"id": id, "text": text, "tags": []}
        for index, entity in enumerate(entities):
            tag = {"category": entity["label"], "start": entity["start_offset"],
                   "mention": text[entity["start_offset"]: entity["end_offset"]]}
            st_item["tags"].append(tag)
        st_data.append(st_item)

    os.makedirs(output, exist_ok=True)
    save_path = os.path.join(output, file_name)
    with open(save_path, "w", encoding="utf-8") as fw:
        for item in st_data:
            fw.write(json.dumps(item, ensure_ascii=False))
            fw.write("\n")
    logger.info("转换结果已保存至 {}".format(output))


if __name__ == '__main__':
    print("start")
