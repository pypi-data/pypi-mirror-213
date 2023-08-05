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

import json
import os
# import sys
import pandas as pd
import numpy as np

# from loguru import logger

from csp.common.utils import read_jsonl


class SpoEva:
    def __init__(self, pre_path, eval_path, long_text_categories=None, output=None):
        self.pre_path = pre_path
        self.eval_path = eval_path
        self.long_text_categories = long_text_categories
        self.output = output
        self.true_data = None
        self.pred_data = None
        self.true_data_dict = None
        self.pred_data_dict = None

    def get_data(self):
        self.true_data = read_jsonl(self.eval_path)
        self.pred_data = read_jsonl(self.pre_path)

        """
        {"id1": {"r1": [spo1, spo2], "r2": [spo3, spo4]}
        """

        self.true_data_dict = self.drop_data(self.true_data)
        self.pred_data_dict = self.drop_data(self.pred_data)

    def drop_data(self, data):
        n_data = {}
        for item in data:
            id = item["id"]
            spo_list = item["spo_list"]
            if n_data.get(id, None) is None:
                n_data[id] = {}
            for spo in spo_list:
                relation = spo["relation"]
                if n_data[id].get(relation, None) is None:
                    n_data[id][relation] = [spo]
                else:
                    n_data[id][relation].append(spo)
        return n_data

    def eva(self):
        self.get_data()

        series = []
        final_precision = 0
        final_recall = 0
        final_f_score = 0
        relation_l = []
        relation_score_dict = {}

        for id, id_info in self.true_data_dict.items():

            pred_id = self.pred_data_dict[id]
            for relation, spo_l in id_info.items():
                pred_id_relation_spo_l = pred_id[relation]

                true_set = set([json.dumps(r) for r in spo_l])
                pred_set = set([json.dumps(r) for r in pred_id_relation_spo_l])
                tp_relation = len(true_set & pred_set)
                precision = round(tp_relation / len(pred_set), 6)
                recall = round(tp_relation / len(true_set), 6)
                if (precision + recall) > 0:
                    f_score = 2 * precision * recall / (precision + recall)
                else:
                    f_score = 0

                if not relation in relation_l:
                    relation_l.append(relation)

                if relation_score_dict.get(relation, None) is None:
                    relation_score_dict[relation] = {"relation_precision_l": [precision],
                                                     "relation_recall_l": [recall],
                                                     "relation_f_score_l": [f_score]}
                else:
                    relation_score_dict[relation]["relation_precision_l"].append(precision)
                    relation_score_dict[relation]["relation_recall_l"].append(recall)
                    relation_score_dict[relation]["relation_f_score_l"].append(f_score)

        for k, v in relation_score_dict.items():
            relation_precision = np.mean(v["relation_precision_l"])
            relation_recall = np.mean(v["relation_recall_l"])
            relation_f_score = np.mean(v["relation_f_score_l"])

            final_precision += relation_precision
            final_recall += relation_recall
            final_f_score += relation_f_score

            result = {"relation": k,
                      "precision": relation_precision,
                      "recall": relation_recall,
                      "f_score": relation_f_score}
            series.append(result)

        final_precision = round(final_precision / len(relation_l), 6)
        final_recall = round(final_recall / len(relation_l), 6)
        final_f_score = round(final_f_score / len(relation_l), 6)
        result = {"relation": "total",
                  "precision": final_precision,
                  "recall": final_recall,
                  "f_score": final_f_score}
        series.append(result)

        result_df = pd.DataFrame(series)
        print(result_df)
        output_eval = os.path.join(self.output, "eval.csv")
        result_df.to_csv(output_eval, sep=",", encoding="utf-8", index=False)


def spo_eva(pre_path, eval_path, output, long_text_categories=None):
    spoeva = SpoEva(pre_path, eval_path, long_text_categories, output=output)
    spoeva.eva()


if __name__ == '__main__':
    print("SUCCESS")
