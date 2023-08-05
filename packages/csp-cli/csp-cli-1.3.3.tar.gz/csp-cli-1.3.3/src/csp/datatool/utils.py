#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/4/24 15:28
# @Author  : xgy
# @Site    : 
# @File    : utils.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import json
import os
import sys

import chardet
import numpy as np
from loguru import logger

# import shutil
# import traceback

task_l = ["obj_det", "img_cls", "text_entity_extra", "text_entity_relation_extra", "text_cls", "text_event"]


class JsonLoad:

    def __init__(self, json_path):
        self.file_path = json_path

    def encodetype(self):
        with open(self.file_path, 'rb') as f:
            try:
                data = f.read()
            except Exception as e:
                logger.error(e)
                return False
            f_charInfo = chardet.detect(data)
            # {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
            if f_charInfo["encoding"] != "utf-8":
                logger.warning("文件必须为 utf-8 编码， 而不是 {}".format(f_charInfo["encoding"]))
        return f_charInfo["encoding"]

    @property
    def data(self):
        # encode_type = self.encodetype()
        # if encode_type != "utf-8":
        #     logger.warning("Documents shall be encoded in UTF-8 format not {}".format(encode_type))
        try:
            with open(self.file_path, "r", encoding="utf-8") as fr:
                json_data = json.load(fr)
            return json_data
        except Exception as e:
            # print(traceback.print_exc())
            print("json 文件错误")
            return None


class EntityBak:

    def __init__(self, folder, output=None):
        self.folder = folder
        self.output = output if output else "./"
        self.label_categories_data = None
        self.labels_data = None
        self.sources_data = None
        self.connections_data = None
        self.connection_categories_data = None
        self.src_ids = []
        self.cate_ids = []
        self.cate_l = []
        self.conn_cate_ids = []

    def get_dataset(self):
        abs_path = os.path.abspath(self.folder)
        self.label_categories_path = os.path.join(abs_path, "labelCategories.json")
        self.labels_path = os.path.join(abs_path, "labels.json")
        self.sources_path = os.path.join(abs_path, "sources.json")
        self.connections_path = os.path.join(abs_path, "connections.json")
        self.connection_categories_path = os.path.join(abs_path, "connectionCategories.json")

        self.label_categories_data = JsonLoad(self.label_categories_path).data
        self.labels_data = JsonLoad(self.labels_path).data
        self.sources_data = JsonLoad(self.sources_path).data

        if os.path.exists(self.connections_path) and os.path.exists(self.connection_categories_path):
            self.connections_data = JsonLoad(self.connections_path).data
            self.connection_categories_data = JsonLoad(self.connection_categories_path).data

    def get_sources_ids(self):
        for item in self.sources_data:
            self.src_ids.append(item["id"])

    def get_cate_ids(self):
        for item in self.label_categories_data:
            self.cate_ids.append(item["id"])
            self.cate_l.append(item["text"])

    def get_conn_cate_ids(self):
        for item in self.connection_categories_data:
            self.conn_cate_ids.append(item["id"])

    def check_json(self, data):
        if data is None or not data:
            return False
        else:
            return True

    def clean_output(self):
        # shutil.rmtree(self.output)
        txt_l = ["connections_srcid_error.txt", "connections_categoryid_error.txt", "connectioncategory_error.txt",
                 "file_error.txt", "sources_error.txt", "labelcategory_error.txt", "labels_srcid_error.txt",
                 "labels_categoryid_error.txt"]
        for item in os.listdir(self.output):
            if item in txt_l:
                re_path = os.path.join(self.output, item)
                os.remove(re_path)

        os.makedirs(self.output, exist_ok=True)


class EntityCheckBack(EntityBak):

    def __init__(self, folder, output=None):
        super(EntityCheckBack, self).__init__(folder, output)

    def check_sources(self):
        """
        公共检查，sources.json 字段值为空
        :return:
        """
        sources_error_l = []
        # 检查字段全为空为空

        sources_flg = True

        for index, item in enumerate(self.sources_data):
            if item["id"]:
                if not item["title"] or not item["content"]:
                    error_item = {"message": "'title' 或 'content' 字段为空", "data": {"id": item["id"]}}
                    sources_error_l.append(error_item)
            else:
                logger.error("'sources' 信息为空")
                error_item = {"message": "'title' 或 'content' 字段为空", "data": item}
                sources_error_l.append(error_item)
                # sources_flg = False

        if sources_error_l:
            save_path = os.path.join(self.output, "sources_error.txt") if self.output else "sources_error.txt"
            with open(save_path, "w", encoding="utf-8") as fw:
                for item in sources_error_l:
                    fw.write(json.dumps(item, ensure_ascii=False))
                    fw.write("\n")
                logger.error("sources.json 有关错误已保存至 {}".format(save_path))
            sources_flg = False
        else:
            if sources_flg:
                logger.info("sources.json 文件中未检测出错误")

        return sources_flg

    def check_labelcategory(self):
        """
        公共检查，labelcategory.json 字段值为空
        :return:
        """
        labelcategorys_flg = True

        labelcategory_error_l = []
        # 检查字段全为空为空

        for item in self.label_categories_data:
            if not item["id"] and not item["text"]:
                logger.error("labelcategory.json 中部分字段为空")
                error_item = {"message": "'text' 字段为空", "data": {"id": item["id"]}}
                labelcategory_error_l.append(error_item)
                # labelcategorys_flg = False
            if item["id"] and not item["text"]:
                error_item = {"message": "'text' 字段为空", "data": {"id": item["id"]}}
                labelcategory_error_l.append(error_item)
            if not item["id"] and item["text"]:
                error_item = {"message": "'id' 字段为空", "data": {"id": item["id"]}}
                labelcategory_error_l.append(error_item)

        if labelcategory_error_l:
            save_path = os.path.join(self.output, "labelcategory_error.txt") if self.output else "labelcategory_error.txt"
            with open(save_path, "w", encoding="utf-8") as fw:
                for item in labelcategory_error_l:
                    fw.write(json.dumps(item, ensure_ascii=False))
                    fw.write("\n")
                logger.error("labelcategories.json 有关错误已保存至  {}".format(save_path))
            labelcategorys_flg = False
        else:
            if labelcategorys_flg:
                logger.info("labelcategories.json 文件中未检测出错误")
        return labelcategorys_flg

    def check_labels(self):
        srcId_error_l = []
        categoryId_error_l = []
        self.get_sources_ids()
        self.get_cate_ids()
        for index, item in enumerate(self.labels_data):
            if item["srcId"] not in self.src_ids:
                error_item = {"message": "", "data": item}
                srcId_error_l.append(error_item)
            if item["categoryId"] not in self.cate_ids:
                error_item = {"message": "sources.json 中无 'categoryId' 字段", "data": item}
                categoryId_error_l.append(error_item)
            # 兼容文本分类任务的labels.json格式
            category_name = item.get("value", 0)
            if not category_name and category_name != 0:
                error_item = {"message": "'category' 值为空", "data": item}
                categoryId_error_l.append(error_item)
            if category_name and (category_name not in self.cate_l):
                error_item = {"message": "'category' 字段值不在 {} 中".format(self.label_categories_path), "data": item}
                categoryId_error_l.append(error_item)

        if srcId_error_l:
            save_path = os.path.join(self.output, "labels_srcid_error.txt") if self.output else "labels_srcid_error.txt"
            with open(save_path, "w", encoding="utf-8") as fw:
                for item in srcId_error_l:
                    fw.write(json.dumps(item, ensure_ascii=False))
                    fw.write("\n")
                logger.error("'srcId' 有关错误已保存至 {}".format(save_path))
        if categoryId_error_l:
            save_path = os.path.join(self.output, "labels_categoryid_error.txt") if self.output else "labels_categoryid_error.txt"
            with open(save_path, "w", encoding="utf-8") as fw:
                for item in categoryId_error_l:
                    fw.write(json.dumps(item, ensure_ascii=False))
                    fw.write("\n")
                logger.error("'categoryId' 有关错误已保存至 {}".format(save_path))
        if not srcId_error_l and not categoryId_error_l:
            logger.info("labels.json 文件中未检测出错误")

    def check_json(self, data=None):
        is_json_sources = super().check_json(self.sources_data)
        is_json_labels = super().check_json(self.labels_data)
        is_json_labelcategories = super().check_json(self.label_categories_data)

        save_path = os.path.join(self.output, "file_error.txt") if self.output else "file_error`.txt`"
        if not is_json_sources:
            with open(save_path, "a+", encoding="utf-8") as fw:
                error_item = {"file_name": self.sources_path, "message": "文件无法加载或为空"}
                fw.write(json.dumps(error_item, ensure_ascii=False))
                fw.write("\n")

        if not is_json_labels:
            with open(save_path, "a+", encoding="utf-8") as fw:
                error_item = {"file_name": self.labels_path, "message": "文件无法加载或为空"}
                fw.write(json.dumps(error_item, ensure_ascii=False))
                fw.write("\n")

        if not is_json_labelcategories:
            with open(save_path, "a+", encoding="utf-8") as fw:
                error_item = {"file_name": self.label_categories_path, "message": "文件无法加载或为空"}
                fw.write(json.dumps(error_item, ensure_ascii=False))
                fw.write("\n")

        if not is_json_sources or not is_json_labels or not is_json_labelcategories:
            logger.error("json 文件错误已保存至 {}".format(save_path))
            return False
        else:
            return True


class EntitySplitBack(EntityBak):

    def __init__(self, folder, output=None):
        super(EntitySplitBack, self).__init__(folder, output)
        self.output = output if output else self.folder

    def filter_by_scr(self, ratio=0.9):
        self.get_sources_ids()
        size = len(self.src_ids)
        filter = Filter(size)
        index_train = filter.choice_random(ratio=ratio)

        source_train = []
        source_test = []
        test_id = []
        for index, item in enumerate(self.sources_data):
            if index in index_train:
                source_train.append(item)
            else:
                source_test.append(item)
                test_id.append(item["id"])

        label_train = []
        label_test = []
        for label in self.labels_data:
            srcId = label["srcId"]
            if srcId in test_id:
                label_test.append(label)
            else:
                label_train.append(label)

        if self.output:
            output_train = os.path.join(self.output, "train")
            output_val = os.path.join(self.output, "eval")
        else:
            output_train = os.path.join(self.folder, "train")
            output_val = os.path.join(self.folder, "eval")

        os.makedirs(output_train, exist_ok=True)
        os.makedirs(output_val, exist_ok=True)

        labels_train_path = os.path.join(output_train, "labels.json")
        sources_train_path = os.path.join(output_train, "sources.json")
        labelCategories_train_path = os.path.join(output_train, "labelCategories.json")

        labels_val_path = os.path.join(output_val, "labels.json")
        sources_val_path = os.path.join(output_val, "sources.json")
        labelCategories_test_path = os.path.join(output_val, "labelCategories.json")

        data_dict = {labels_train_path: label_train,
                     sources_train_path: source_train,
                     sources_val_path: source_test,
                     labels_val_path: label_test,
                     labelCategories_train_path: self.label_categories_data,
                     labelCategories_test_path: self.label_categories_data}

        for k, v in data_dict.items():
            # file_name = k + ".json"
            # output_item = os.path.join(self.output, file_name) if self.output else os.path.join(self.folder, file_name)
            # with open(output_item, "w", encoding="utf-8") as f:
            with open(k, "w", encoding="utf-8") as f:
                json.dump(v, f, ensure_ascii=False, indent=4)
            logger.info("切分结果已保存至 {}".format(k))

        return source_train, source_test


class Entity:

    def __init__(self, folder, output=None):
        self.folder = folder
        self.output = output if output else "./"
        self.data = None
        self.data_path = None
        self.ids = []
        os.makedirs(output, exist_ok=True)

    def get_dataset(self):
        abs_path = os.path.abspath(self.folder)
        data_path = None
        for root, _, files in os.walk(abs_path):
            if len(files) != 1:
                raise FileExistsError("数据集结构错误, {} 中不止一份文件".format(self.folder))
            for file in files:
                data_path = os.path.join(root, file)
                self.data_path = data_path
        if data_path:
            try:
                with open(data_path, "r", encoding="utf-8") as fr:
                    self.data = []
                    l = fr.readlines()
                    for line in l:
                        self.data.append(json.loads(line))
            except Exception as ae:
                logger.error("json文件错误", ae)
                sys.exit()

    def clean_output(self):
        # shutil.rmtree(self.output)
        txt_l = ["connections_srcid_error.txt", "connections_categoryid_error.txt", "connectioncategory_error.txt",
                 "file_error.txt", "sources_error.txt", "labelcategory_error.txt", "labels_srcid_error.txt",
                 "labels_categoryid_error.txt", "spo_list_null.txt", "id_text_error.txt", "id_error.txt", "text_error.txt",
                 "spo_key_error.txt", "spo_value_error.txt"]
        for item in os.listdir(self.output):
            if item in txt_l:
                re_path = os.path.join(self.output, item)
                os.remove(re_path)

        os.makedirs(self.output, exist_ok=True)

    def check_json(self, data):
        if data is None or not data:
            return False
        else:
            return True

    def get_ids(self):
        for item in self.data:
            if not item["id"]:
                raise ValueError("'id' 字段不能为空", item)
            self.ids.append(item["id"])


class TxtFileCheck:

    def __init__(self, folder):
        self.folder = folder

    def txt_file_check(self, output=None):
        """
        判断 txt 文件是否打开异常、是否为 utf-8 编码
        :param output:
        :return:
        """
        txt_file_error_l = []
        abs_path = os.path.abspath(self.folder)
        for root, _, files in os.walk(abs_path):
            for file in files:
                txt_path = os.path.join(root, file)
                txt_ = JsonLoad(txt_path)
                file_encode = txt_.encodetype()
                if not file_encode:
                    logger.error("{} 无法打开".format(txt_path))
                    txt_file_error_l.append(txt_path)
                else:
                    if file_encode != "utf-8":
                        txt_file_error_l.append(txt_path)
                        logger.error("文件必须为 'UTF-8' 编码, 而 {} 为 {} 编码".format(txt_path, file_encode))
        if txt_file_error_l:
            save_path = os.path.join(output, "txt_file_error.txt") if output else "txt_file_error.txt"
            with open(save_path, "w", encoding="utf-8") as fw:
                for item in txt_file_error_l:
                    fw.write(item + "\n")
            logger.info("检查结果已保存至 {}".format(save_path))
        else:
            logger.info("txt 文件中未检测出错误")


class Filter:

    def __init__(self, size):
        self.size = size

    def choice_random(self, ratio: float, seed=2):
        assert 0 < ratio <= 1, "ratio 值必须介于0-1 (0<ratio<=1)"
        np.random.seed(seed)
        num = int(self.size * ratio)
        filter_index = np.random.choice(self.size, num, replace=False)
        return list(filter_index)


if __name__ == '__main__':
    print("start")
