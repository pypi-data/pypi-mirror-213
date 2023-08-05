#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/6/23 9:24
# @Author  : xgy
# @Site    : 
# @File    : transform.py
# @Software: PyCharm
# @python version: 3.7.4
"""

from csp.datatool.text_entity_relation.spo_utils.standard2doccano import standard2doccno
from csp.datatool.text_entity_relation.spo_utils.uiespo2standard import uiespo2standard
from csp.datatool.text_entity_relation.spo_utils.standard2kg import ud2table


def spo_transform(folder, form, output, uie_file=None):
    if form.lower() == "standard2doccano":
        standard2doccno(folder, output)
    elif form.lower() == "uie2standard":
        uiespo2standard(uie_file, folder, output)
    elif form.lower() == "standard2kg":
        ud2table(folder, output)
    else:
        raise KeyError("from 参数必须为 standard2doccano/uie2standard/standard2kg 之一")


if __name__ == '__main__':
    print("start")
