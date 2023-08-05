#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/9/27 8:50
# @Author  : xgy
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @python version: 3.7.4
"""

from csp.topic.topic_server import topic_list as list
from csp.topic.topic_server import topic_download as download
from csp.topic.topic_server import topic_upload as upload
from csp.topic.topic_server import topic_info as info
from csp.topic.topic_server import topic_find as find
# from csp.topic.model_server import model_start as start
# from csp.topic.model_server import model_eva as eva


if __name__ == '__main__':
    print("start")
