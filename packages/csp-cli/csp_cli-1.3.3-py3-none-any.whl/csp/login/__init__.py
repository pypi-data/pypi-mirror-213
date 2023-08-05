#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/11/16 11:25
# @Author  : xgy
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @python version: 3.7.13
"""

from csp.login.login_server import user_login as login
from csp.login.login_server import check_user
from csp.login.login_server import user_logout as logout
from csp.login.login_server import re_login as relogin
from csp.login.login_server import user_register as register

if __name__ == '__main__':
    print("start")
