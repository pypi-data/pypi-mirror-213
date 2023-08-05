#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/6/21 15:59
# @Author  : xgy
# @Site    : 
# @File    : check.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import json
import os

from loguru import logger

from csp.datatool.text_entity.check_bak import EntityCheck


class SpoCheck(EntityCheck):
    
    def __init__(self, folder, output=None):
        super(SpoCheck, self).__init__(folder, output)

    def check_connections(self):
        """
        检查 connections.json
        """
        srcId_error_l = []
        categoryId_error_l = []
        self.get_sources_ids()
        self.get_conn_cate_ids()
        for index, item in enumerate(self.connections_data):
            if item["srcId"] not in self.src_ids:
                error_item = {"message": "sources.json 不存在 'srcId' 字段", "data": item}
                srcId_error_l.append(error_item)
            if item["categoryId"] not in self.conn_cate_ids:
                error_item = {"message": "connectionCategories.json 不存在 'categoryId' 字段", "data": item}
                categoryId_error_l.append(error_item)

        if srcId_error_l:
            save_path = os.path.join(self.output, "connections_srcid_error.txt") if self.output else "connections_srcid_error.txt"
            with open(save_path, "w", encoding="utf-8") as fw:
                for item in srcId_error_l:
                    fw.write(json.dumps(item, ensure_ascii=False))
                    fw.write("\n")
                logger.error("sources.json 有关错误已保存至 {}".format(save_path))
        if categoryId_error_l:
            save_path = os.path.join(self.output, "connections_categoryid_error.txt") if self.output else "connections_categoryid_error.txt"
            with open(save_path, "w", encoding="utf-8") as fw:
                for item in categoryId_error_l:
                    fw.write(json.dumps(item, ensure_ascii=False))
                    fw.write("\n")
                logger.error("connections.json 有关错误已保存至 {}".format(save_path))
        if not srcId_error_l and not categoryId_error_l:
            logger.info("connections.json 中未检测出错误")

    def check_connectioncategory(self):
        """
        公共检查，connectioncategory.json 字段值为空
        :return:
        """
        connectioncategorys_flg = True
        connection_category_error_l = []
        # 检查字段全为空为空
        for item in self.connection_categories_data:
            if not item["id"] and not item["text"]:
                logger.error("一些关系标签为空")
                error_item = {"message": "一些关系标签为空", "data": item}
                connection_category_error_l.append(error_item)
                # connectioncategorys_flg = False
            if item["id"] and not item["text"]:
                error_item = {"message": "'text' 字段为空", "data": {"id": item["id"]}}
                connection_category_error_l.append(error_item)
                # connectioncategorys_flg = False
            if not item["id"] and item["text"]:
                error_item = {"message": "'id' 字段为空", "data": item}
                connection_category_error_l.append(error_item)

        if connection_category_error_l:
            save_path = os.path.join(self.output, "connectioncategory_error.txt") if self.output else "connectioncategory_error.txt"
            with open(save_path, "w", encoding="utf-8") as fw:
                for item in connection_category_error_l:
                    fw.write(json.dumps(item, ensure_ascii=False))
                    fw.write("\n")
                logger.error("connectionCategories.json 有关错误已保存至 {}".format(save_path))
            connectioncategorys_flg = False
        else:
            if connectioncategorys_flg:
                logger.info("connectioncategory.json  中未检测出错误")
        return connectioncategorys_flg

    def check_json(self, data=None):
        flag_super = super(SpoCheck, self).check_json()
        is_json_connections = super(EntityCheck, self).check_json(self.connections_data)
        is_json_connectioncategories = super(EntityCheck, self).check_json(self.connection_categories_data)

        save_path = os.path.join(self.output, "file_error.txt") if self.output else "file_error.txt"
        if not is_json_connections:
            with open(save_path, "a+", encoding="utf-8") as fw:
                error_item = {"file_name": self.connections_path,
                              "message": "文件无法加载或为空"}
                fw.write(json.dumps(error_item, ensure_ascii=False))
                fw.write("\n")

        if not is_json_connectioncategories:
            with open(save_path, "a+", encoding="utf-8") as fw:
                error_item = {"file_name": self.connection_categories_path, "message": "文件无法加载或为空"}
                fw.write(json.dumps(error_item, ensure_ascii=False))
                fw.write("\n")

        if not flag_super or not is_json_connections or not is_json_connectioncategories:
            logger.error("json 文件有关错误已保存至 {}".format(save_path))
            return False
        else:
            return True


def spo_check(folder, output=None):
    if output:
        os.makedirs(output, exist_ok=True)
    check_relation = SpoCheck(folder, output=output)
    check_relation.clean_output()
    check_relation.get_dataset()

    # 第一步判断json文件是否能打开
    flag_json = check_relation.check_json()

    if flag_json:
        flag_sources = check_relation.check_sources()
        flag_labelcategory = check_relation.check_labelcategory()
        flag_connetioncategory = check_relation.check_connectioncategory()

        if flag_sources and flag_labelcategory and flag_connetioncategory:
            check_relation.check_labels()
            check_relation.check_connections()
        else:
            logger.warning("{} 或 {} 或 {} 存在错误. labels.json 和 connections.json 将不会执行检查".format(
                check_relation.sources_path, check_relation.label_categories_path, check_relation.connection_categories_path))


if __name__ == '__main__':
    print("start")
