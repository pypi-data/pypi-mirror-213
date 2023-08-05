#!/usr/bin/env python
# encoding: utf-8  
from csp.command.cli import csptools 
# 一级命令 csp pipeline
@csptools.group("pipeline")
def pipeline():
    """
    流水线框架命令，包括uie训练流程、目标检测模型训练等子命令

    \b
    csp pipeline 'commands' -h 获取子命令使用帮助
    """


if __name__ == '__main__':
    print("start")
