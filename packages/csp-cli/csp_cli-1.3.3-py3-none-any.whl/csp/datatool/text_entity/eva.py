#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/4/27 9:50
# @Author  : xgy
# @Site    : 
# @File    : eva.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import os
import sys
import json
import pandas as pd
# import numpy as np
from loguru import logger

from csp.common.utils import read_jsonl


class EntityEva:

    def __init__(self, pre_path, eval_path, long_text_categories=None, output=None):
        self.pre_path = pre_path
        self.eval_path = eval_path
        self.long_text_categories = long_text_categories
        self.output = output
        self.pred_dict = {}
        self.true_dict = {}

    @staticmethod
    def list_category_values(category, df):
        """
        将tag中一个元素（{}）转为字符串，用于后续匹配判断正误
        拼接元素包含 "id + mention + start"
        :return:
        """
        values = []
        df_category = df[df["category"] == category].reset_index(drop=True)
        len_category = len(df_category)
        for _, row in df_category.iterrows():
            key = str(row["id"]) + str(row["mention"]) + str(row["start"])
            values.append(key)

        return values, len_category

    @staticmethod
    def calculate(y_true, y_pred, len_true, len_pred):
        """
        计算 precision, recall
        """
        precision = 0
        recall = 0

        tp_count = 0
        if y_true and y_pred:
            for pred in y_pred:
                if pred in y_true:
                    tp_count += 1

            precision = round(tp_count / len_pred, 3)
            recall = round(tp_count / len_true, 3)

        return precision, recall

    def df_proc(self, df):
        df_source_spilt = self.df_source[["id", "text"]]
        df = pd.merge(df, df_source_spilt, left_on="id", right_on='id', how="inner")
        return df

    def evaluate(self, output_eval):
        series = []
        final_precision = 0
        final_recall = 0
        final_f_score = 0
        for category in self.categories:

            y_true, len_true = self.list_category_values(category, self.df_true)
            y_pred, len_pred = self.list_category_values(category, self.df_pred)

            if not len_true:
                logger.warning("标签 {} 在 {} 中不存在".format(category, self.eval_path))
            if not len_pred:
                logger.warning("标签 {} 在 {} 中不存在".format(category, self.pre_path))

            if len_true and len_pred:
                precision, recall = self.calculate(y_true, y_pred, len_true, len_pred)
            else:
                precision, recall = 0, 0

            final_precision += precision
            final_recall += recall
            f_score = 0
            if (precision + recall) > 0:
                f_score = 2 * precision * recall / (precision + recall)
            final_f_score += f_score
            result = {"category": category,
                      "precision": round(precision, 3),
                      "recall": round(recall, 3),
                      "f_score": round(f_score, 3)}
            series.append(result)
        final_precision = round(final_precision / len(self.categories), 3)
        final_recall = round(final_recall / len(self.categories), 3)
        final_f_score = round(final_f_score / len(self.categories), 3)
        result = {"category": "total",
                  "precision": final_precision,
                  "recall": final_recall,
                  "f_score": final_f_score}
        series.append(result)

        result_df = pd.DataFrame(series)
        # print(result_df)
        result_df.to_csv(output_eval, sep=",", encoding="utf-8", index=False)

        title_dict = {"类别": "category", "召回率": "recall", "准确率": "precision", "f1": "f_score"}
        result_dict = {"data": series}
        from csp.common.utils import format
        format(result_dict, title_dict)

    def get_data(self):
        # 固定列顺序
        true_data = read_jsonl(self.eval_path)
        pred_data = read_jsonl(self.pre_path)

        categories = []
        true_tags = []
        text_sources = []
        for item in true_data:
            tags = item["tags"]
            text = item["text"]
            self.true_dict[item["id"]] = item
            for tag in tags:
                tag["id"] = item["id"]
                true_tags.append(tag)
                category = tag["category"]
                if category not in categories:
                    categories.append(category)
            result_sources = {"id": item["id"], "text": text}
            text_sources.append(result_sources)

        pred_tags = []
        for item in pred_data:
            tags = item["tags"]
            self.pred_dict[item["id"]] = item
            for tag in tags:
                tag["id"] = item["id"]
                pred_tags.append(tag)

        true_raw = pd.DataFrame(true_tags)[["id", "category", "start", "mention"]]
        pred_raw = pd.DataFrame(pred_tags)[["id", "category", "start", "mention"]]
        df_source = pd.DataFrame(text_sources)[["id", "text"]]

        self.true_raw = true_raw
        self.pred_raw = pred_raw
        self.df_source = df_source
        self.categories = categories

        return true_raw, pred_raw

    def data_filter_by_igcategory(self):
        logger.info("以下长文本字段将被忽略 {}".format(self.long_text_categories))

        if not self.long_text_categories:
            self.df_true = self.true_raw
            self.df_pred = self.pred_raw
        else:
            # tod 有问题
            for item in self.long_text_categories:
                self.df_true = self.true_raw[self.true_raw["category"] != item]
            for item in self.long_text_categories:
                self.df_pred = self.pred_raw[self.pred_raw["category"] != item]

    def get_badcase(self):
        list_good = []
        list_bad = []
        true_keys = []
        true_keys_l = []
        for _, row_true in self.df_true.iterrows():
            # row_true_split = list(row_true)[1:4]
            row_true_split = list(row_true)[0:4]
            row_true_str = []
            for item in row_true_split:
                item_str = str(item)
                row_true_str.append(item_str)
            key_true = "_".join(row_true_str)
            true_keys.append(key_true)
            true_keys_l.append(row_true_split)

        pred_keys = []
        pred_keys_l = []
        for _, row_pred in self.df_pred.iterrows():
            # row_pred_split = list(row_pred)[1:4]
            row_pred_split = list(row_pred)[0:4]
            row_pred_str = []
            for item in row_pred_split:
                item_str = str(item)
                row_pred_str.append(item_str)
            key_pred = "_".join(row_pred_str)
            pred_keys.append(key_pred)
            pred_keys_l.append(row_pred_split)

            if key_pred in true_keys:
                list_good.append(list(row_pred))
            else:
                list_bad.append(list(row_pred))

        json_good = {}
        json_bad = {}
        for item_true in true_keys_l:
            item_id = item_true[0]
            str_item_true = "_".join([str(x) for x in item_true])
            data_id = self.true_dict[item_id]
            if not json_bad.get(item_id, None):
                json_bad[item_id] = {"id": data_id["id"],
                                     "text": data_id["text"],
                                     "tags": data_id["tags"],
                                     "new": [],
                                     "wrong": []}
            if not json_good.get(item_id, None):
                json_good[item_id] = {"id": data_id["id"],
                                      "text": data_id["text"],
                                      "tags": data_id["tags"],
                                      "true": []}

            if str_item_true not in pred_keys:
                json_bad[item_id]["wrong"].append({"category": item_true[1],
                                                   "start": item_true[2],
                                                   "mention": item_true[3]})
            else:
                json_good[item_id]["true"].append({"category": item_true[1],
                                                   "start": item_true[2],
                                                   "mention": item_true[3]})
        for item_pred in pred_keys_l:
            item_id = item_pred[0]
            str_item_pred = "_".join([str(x) for x in item_pred])
            data_id = self.true_dict[item_id]
            if not json_bad.get(item_id, None):
                json_bad[item_id] = {"id": data_id["id"],
                                     "text": data_id["text"],
                                     "tags": data_id["tags"],
                                     "new": [],
                                     "wrong": []}

            if str_item_pred not in true_keys:
                json_bad[item_id]["new"].append({"category": item_pred[1],
                                                 "start": item_pred[2],
                                                 "mention": item_pred[3]})

        col_names = ["id", "category", "start", "mention"]
        df_good = self.df_proc(pd.DataFrame(list_good, columns=col_names))
        df_bad = self.df_proc(pd.DataFrame(list_bad, columns=col_names))

        json_bad_l = []
        json_good_l = []
        for k, v in json_good.items():
            json_good_l.append(v)
        for k, v in json_bad.items():
            json_bad_l.append(v)

        return df_good, df_bad, json_good_l, json_bad_l

    @staticmethod
    def df2files(df, json_data, output_json, output_excel):
        # df.to_json(output_json, orient="records", force_ascii=False, indent=4)
        with open(output_json, "w", encoding="utf-8") as fw:
            json.dump(json_data, fw, ensure_ascii=False, indent=4)
        # df.to_excel(output_excel, index=False)


def print_error_msg(msg, code):
    result_json = {}
    result_json['error_msg'] = msg
    result_json['error_code'] = code
    # result_json['usage'] = usage
    print(json.dumps(result_json, ensure_ascii=False))


def entity_eva(pre_path, eval_path, output, long_text_categories=None):
    if not os.path.exists(pre_path) or not os.path.isfile(pre_path):
        print_error_msg(("未找到待评估的预测结果文件: %s" % pre_path), 1001)
        sys.exit(1)

    if not os.path.exists(eval_path) or not os.path.isfile(eval_path):
        print_error_msg(("未找到标注测试集文件: %s" % eval_path), 1002)
        sys.exit(1)

    os.makedirs(output, exist_ok=True)

    output_good_json = os.path.join(output, "good.json")
    output_bad_json = os.path.join(output, "bad.json")
    output_good_excel = os.path.join(output, "good.xlsx")
    output_bad_excel = os.path.join(output, "bad.xlsx")
    output_eval = os.path.join(output, "result.csv")

    entityeva = EntityEva(pre_path, eval_path, long_text_categories, output=output)
    entityeva.get_data()
    entityeva.data_filter_by_igcategory()
    df_good, df_bad, json_good, json_bad = entityeva.get_badcase()

    entityeva.df2files(df_good, json_good, output_good_json, output_good_excel)
    entityeva.df2files(df_bad, json_bad, output_bad_json, output_bad_excel)

    entityeva.evaluate(output_eval)
    print("评估结果及badcase分析已保存至： {}".format(output))


if __name__ == '__main__':
    print("start")

