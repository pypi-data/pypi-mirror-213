"""
子模块读取工具
"""
from importlib import import_module
from sys import path as sys_path


class ReadModule:
    def __init__(self, path=None):
        """
        对象初始化
        :param path: 要读取的子模块路径
        """
        sys_path.append('..' if path is None else path)
        self.module_list = {}

    def read(self, item):
        """
        要读取的子模块
        :param item: 子模块名称
        :return: 子模块
        """
        if item not in self.module_list.keys():
            self.module_list[item] = import_module(item)
        return self.module_list[item]
