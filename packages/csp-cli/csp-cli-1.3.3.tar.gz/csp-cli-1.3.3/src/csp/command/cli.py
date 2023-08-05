#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/3/25 9:34
# @Author  : xgy
# @Site    : 
# @File    : cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os
import sys

import click

from csp.common.utils import RunSys

# 与setup.py中版本同步修改
__version__ = "1.3.3"
pgk_dir = os.path.join(os.path.dirname(os.path.abspath('__file__')))
param_decls = ["-V", "--version", "--VERSION"]


# 主组命令 csp
# 在setup的entry_points字段中指定
@click.group(context_settings={'help_option_names': ['-h', '--help']}, invoke_without_command=True)
@click.version_option('{0} from {1} (Python {2})'.format(__version__, pgk_dir, sys.version[:3]), *param_decls)
def csptools():
    """
    csp 命令行工具；

    \b
    csp 'commands' -h 获取子命令使用帮助
    """
    if len(sys.argv) == 1:
        cmd = "csp -h"
        status = RunSys(command=cmd).run_cli()
        if status:
            print("csp-cli installed successful")
        else:
            print("csp-cli installed unsuccessful")


# @csptools.command()
# def cmd1():
#     """Command on cli1"""
#     print("cli1 cmd1")

# @csptools.command()
# @click.option("-u", "--username", prompt="用户名", help="用户名", required=True)
# @click.option("-p", "--passwd", prompt="密码", help="密码", required=True, hide_input=True, confirmation_prompt=True)
# def login(username, passwd):
#     """
#     用户登录命令
#
#     \b
#     csp login -h 获取帮助
#     """