#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/8/22 14:51
# @Author  : xgy
# @Site    : 
# @File    : eva.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import json
import os
import numpy as np


def read_json(file):
    if not file.endswith(".json") or not os.path.exists(file):
        raise Exception('文件不存在或非json文件 %s' % file)

    with open(file, "r", encoding="utf-8") as fr:
        data = []
        l = fr.readlines()
        for line in l:
            data.append(json.loads(line))
    return data


def calc_score(candidate, refs):
    """
    得分计算
    Args:
        candidate (): 预测结果
        refs (): 标准答案

    Returns: dict 总得分，模式得分

    计算步骤
    1. 单一预测（一条预测结果mentions列表中的一个元素）得分，采用lcs计算得分
    2. 单一文本得分（一条文本可能含多个预测结果（故事））
    3. 单一模式得分（一个模式schema含多条文本）
    4. 总得分score（四个模式加权平均得分）
    """
    key_refs = ["id", "schema", "text", "mentions"]
    # schema_refs = ["A域调度指令", "B域调度指令", "X类系统装置功能", "Y类控制要求"]
    schema_refs = []
    # 将refs由列表转为以id为键的字典
    refs_dict = {}
    # 计算标准答案中每个schema包含的故事总数
    schema_result_num = {}
    for item_r in refs:
        refs_dict[item_r["id"]] = item_r
        sch = item_r["schema"]
        men = item_r["mentions"]
        len_men = len(men)
        if not schema_result_num.get(sch, None):
            schema_result_num[sch] = len_men
        else:
            schema_result_num[sch] = len_men + schema_result_num[sch]
        if sch not in schema_refs:
            schema_refs.append(sch)

    schema_dict = {}

    # 是否启用相关惩罚系数
    flag_doc = False
    # flag_result = False

    for item_c in candidate:
        # 键值判断
        item_keys = list(item_c.keys())
        for key in item_keys:
            if key not in key_refs:
                raise Exception("KeyError, '{}' 在预测中多出".format(key))

        # 一个item对应一条文本，对应一个id
        # mentions 即待匹配结果列表
        mentions_c = item_c["mentions"]
        if not isinstance(mentions_c, list):
            raise Exception("TypeError, 'mentions' 不是 list")

        id = item_c["id"]
        mentions_r = refs_dict[id]["mentions"]
        len_mentions_c = len(mentions_c)
        len_mentions_r = len(mentions_r)

        if len_mentions_r < len_mentions_c:
            mentions_r, mentions_c = mentions_c, mentions_r
            flag_doc = True

        # 遍历预测结果
        # 遍历一条文本的多个结果
        score_doc = None  # 单条文本得分 = 每条预测结果最佳得分的累和 * 惩罚系数
        if not mentions_c:  # 一条文本的抽取结果为空
            score_doc = 0

        for item_mention_c in mentions_c:
            if not isinstance(item_mention_c, list):
                raise Exception("TypeError, 'mentions' 中的元素不是 list")
            if not item_mention_c:
                raise Exception("ValueError, 'mentions' 中元素的值不能为 [], 请删除")
            # 在标准答案列表 mentions_r 中寻找分数最高的匹配项 item_mention_r
            score_one_result_max = None  # 一条预测结果去匹配所有标准答案的最大分数
            for index, item_mention_r in enumerate(mentions_r):
                score_one_result = None  # 单一预测结果（结果中含多个字段）得分，等于单个字段得分的累积

                if len(item_mention_r) < len(item_mention_c):
                    item_mention_c, item_mention_r = item_mention_c, item_mention_r
                    # flag_result = True

                for result_c in item_mention_c:
                    if not isinstance(result_c, dict):
                        raise Exception("TypeError, 'mentions' 元素的元素不是 dict")
                    keys_result = list(result_c.keys())
                    if sorted(np.unique(keys_result)) != sorted(np.unique(["key", "value"])):
                        raise Exception(
                            '提交文件中存在非法的key %s (correct: keys: %s)' % (
                                keys_result, np.unique(["key", "value"])))

                    key_c = result_c["key"]
                    value_c = result_c["value"]
                    if isinstance(value_c, list):
                        value_c = "".join(value_c)

                    # 当 item_mention_c 与 item_mention_r 中字段数不同时，不能直接赋 0 分， 依旧采用系数惩罚的方式
                    for result_r in item_mention_r:
                        key_r = result_r["key"]
                        if key_r == key_c:
                            value_r = result_r["value"]
                            if isinstance(value_r, list):
                                value_r = "".join(value_r)
                            # todo lcs 算法选择
                            cls = lcs_order(value_c, value_r)
                            # 单一预测中一个字段的得分
                            score_item = round(cls / max(len(value_c), len(value_r)), 4)
                            if score_one_result is None:
                                score_one_result = score_item
                            else:
                                # 一条匹配的分数 = 所有字段得分的乘积
                                # 不能连乘，会导致仅一个字段非常低时，导致整体分数极低，修改为平均
                                # score_one_result = score_one_result * score_item
                                score_one_result = score_one_result + score_item
                            break
                if not score_one_result_max:
                    # if flag_result:
                    #     score_one_result_max = (score_one_result / len(item_mention_c)) * (min(len(item_mention_c), len(item_mention_r)) / max(len(item_mention_c), len(item_mention_r)))  # 一条故事最终得分，需乘以系数惩罚
                    # else:
                    #     score_one_result_max = score_one_result / len(item_mention_c)
                    if score_one_result is None:
                        score_one_result = 0
                    score_one_result_max = (score_one_result / len(item_mention_c)) * (
                            min(len(item_mention_c), len(item_mention_r)) / max(len(item_mention_c),
                                                                                len(item_mention_r)))  # 一条故事最终得分，需乘以系数惩罚

                else:
                    # 一条匹配的最终分数取所有可能匹配的最大分数
                    # if flag_result:
                    #     score_one_result_max = max(score_one_result_max, (score_one_result / len(item_mention_c)) * (min(len(item_mention_c), len(item_mention_r)) / max(len(item_mention_c), len(item_mention_r))))  # 一条故事最终得分，需乘以系数惩罚)
                    # else:
                    #     score_one_result_max = max(score_one_result_max, (score_one_result / len(item_mention_c)))
                    if score_one_result is None:
                        score_one_result = 0
                    score_one_result_max = max(score_one_result_max, (score_one_result / len(item_mention_c)) * (
                            min(len(item_mention_c), len(item_mention_r)) / max(len(item_mention_c),
                                                                                len(item_mention_r))))  # 一条故事最终得分，需乘以系数惩罚)

            if not score_doc:
                if score_one_result_max is None:
                    score_one_result_max = 0
                score_doc = score_one_result_max
            else:
                # 单条文本得分
                if score_one_result_max is None:
                    score_one_result_max = 0
                score_doc = score_doc + score_one_result_max

        # 按 schema 分类, 每一条文本得分需乘以系数惩罚
        schema = item_c["schema"]
        if not schema or schema not in schema_refs:
            raise Exception("ValueError, schema '{}' 在预测中多出".format(schema))
        if not schema_dict.get(schema, None):
            if flag_doc:
                schema_dict[schema] = [score_doc * (min(len_mentions_c, len_mentions_r) / max(len_mentions_c,
                                                                                              len_mentions_r))]  # 单条文本得分 = 每条预测结果最佳得分的累和 * 惩罚系数
            else:
                schema_dict[schema] = [score_doc]
        else:
            if flag_doc:
                schema_dict[schema].append(
                    score_doc * (min(len_mentions_c, len_mentions_r) / max(len_mentions_c, len_mentions_r)))
            else:
                schema_dict[schema].append(score_doc)

    # 计算单一schema得分 = schema相关文档得分的加和
    # 分数加和，不属于[0, 1], 加和除以schema的总故事数 schema_result_num[k]
    score_return = {}
    for sch in schema_refs:
        score_return[sch] = 0
    score_dict = {"score": []}
    for k, v in schema_dict.items():
        score_schema = np.sum(v) / schema_result_num[k]
        score_dict[k] = score_schema
        score_dict["score"].append(score_schema)

        score_return[k] = score_schema

    score_return['score'] = np.mean(score_dict['score'])
    return score_return


def lcs_order(string, sub):
    """
    string 和 sub 的最长公共子序列
    :param string: 字符串1
    :param sub: 字符串2
    :return: 最长公共子序列的长度
    """
    if len(string) < len(sub):
        sub, string = string, sub

    lcs_l = []
    for i in range(len(sub)):
        for j in range(len(sub)):
            pattern = sub[j:len(sub) - i]
            if pattern in string:
                if not lcs_l:
                    lcs_l.append(pattern)
                else:
                    if len(pattern) > len(lcs_l[-1]):
                        lcs_l[-1] = pattern
                    elif len(pattern) == len(lcs_l[-1]):
                        lcs_l.append(pattern)
    if lcs_l:
        len_cls = len(lcs_l[0])
    else:
        len_cls = 0
    return len_cls


def lcs_disorder(string, sub):
    """
    获取长度
    :param string: 字符串1
    :param sub: 字符串2
    :return: 最长公共子序列的长度
    """
    if len(string) < len(sub):
        sub, string = string, sub

    lengths = [[0 for i in range(0, len(sub) + 1)] for j in range(0, len(string) + 1)]

    for j in range(1, len(sub) + 1):
        for i in range(1, len(string) + 1):
            if string[i - 1] == sub[j - 1]:
                lengths[i][j] = lengths[i - 1][j - 1] + 1
            else:
                lengths[i][j] = max(lengths[i - 1][j], lengths[i][j - 1])

    return lengths[len(string)][len(sub)]


def event_eva(submit_file, answer_file):
    """
    算比分
    :param answer_file: 标准答案.json
    :param submit_file: 提交.json
    :return: 得分字典
    """

    # 检查文件后缀是否正确：.json
    # 检查json文件行数是否正确
    # id 完整性检查

    submit_data = read_json(submit_file)
    truth_data = read_json(answer_file)

    # 判断行数和id完整性
    # 行数是否正确
    answer_len = len(truth_data)
    if len(submit_data) != answer_len:
        raise Exception(
            '提交的结果文件的有效行数不正确 '
            '(正确行数为: %s)' % answer_len)

    # id 完整性检查
    submit_ids = []
    truth_ids = []
    for item_s, item_t in zip(submit_data, truth_data):
        submit_ids.append(item_s["id"])
        truth_ids.append(item_t["id"])

    if sorted(np.unique(submit_ids)) != sorted(np.unique(truth_ids)):
        raise Exception('提交的文件包含非法ID (正确id为: %s)' % len(np.unique(truth_ids)))
    scores = calc_score(submit_data, truth_data)
    # try:
    #     scores = calc_score(submit_data, truth_data)
    # except Exception:
    #     raise Exception("calculate system error")
    print(scores)

    return scores


if __name__ == '__main__':
    print("start")
