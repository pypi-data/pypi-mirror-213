#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/11/16 16:42
# @Author  : xgy
# @Site    : 
# @File    : login_cli.py
# @Software: PyCharm
# @python version: 3.7.13
"""

import click
from csp.command.cli import csptools


# 一级命令 csp user
@csptools.group("user")
def user():
    """
    账户操作命令，包括用户登录、登出、注册等子命令

    \b
    csp user 'commands' -h 获取子命令使用帮助
    """


# 二级命令 csp user login
@user.command()
@click.option("-u", "--username", prompt="用户名", help="用户名", required=True)
# @click.option("-p", "--passwd", prompt="密码", help="密码", required=True, hide_input=True, confirmation_prompt=True)
@click.option("-p", "--passwd", prompt="密码", help="密码", required=True, hide_input=True)
def login(username, passwd):
    """
    用户登录命令

    \b
    使用示例：csp user login -u "用户名" -p "用户密码"
    """
    try:
        from csp.login.login_server import user_login
        user_login(username, passwd)
        print("登录成功")
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


# 二级命令 csp user logout
@user.command()
def logout():
    """
    用户退出登录命令

    \b
    使用示例：csp user logout
    """
    try:
        from csp.login.login_server import user_logout
        user_logout()
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


# 二级命令 csp user register
@user.command()
@click.option("-u", "--username", type=click.STRING, prompt="用户名", help="用户名", required=True)
@click.option("-p", "--passwd", type=click.STRING, prompt="密码，至少8位字符", help="密码，至少8位字符", required=True, hide_input=True)
@click.option("-n", "--nickname", type=click.STRING, prompt="显示昵称，请输入中文名", help="显示昵称，请输入中文名", required=True)
def register(username, passwd, nickname):
    """
    用户注册命令

    \b
    使用示例：csp user register -u "用户名" -p "用户密码" -n "显示昵称（中文）"
    """
    if not nickname:
        nickname = None
    try:
        from csp.login.login_server import user_register
        user_register(username, passwd, nickname)
    except KeyError as ke:
        print("KeyError: ", str(ke))
    except Exception as ae:
        print(str(ae))


if __name__ == '__main__':
    print("start")
