#!/usr/bin/env python
# encoding: utf-8
from csp.command.cli import csptools
 
@csptools.group("labeltool")
def labeltool():
    """
    标注工具命令

    \b
    csp labeltool 'commands' -h 获取子命令使用帮助
    """ 