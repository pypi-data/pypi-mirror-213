"""
配置文件读取工具
"""
from eqmicro.components.ext_lib import json_file_read


class ReadConf:
    def __init__(self, file_path):
        """
        对象初始化初始化
        :param file_path: 配置文件路径
        """
        self.conf_path = file_path
        self.configuration = {}

    def __read__(self, node):
        """
        配置项读取
        :param node: 配置项，如 a.b.c
        """
        if bool(self.configuration) is False:  # 先判断 configuration 是否有内容，无内容则先加载配置文件
            self.configuration = json_file_read(self.conf_path)
        items = node.split('.')
        return self.__item_read__(items)

    def __file_load__(self):
        """
        配置文件加载
        """
        if bool(self.configuration) is False:
            self.configuration = json_file_read(self.conf_path)

    def __item_read__(self, items):
        """
        按层级读取配置项
        :param items: 配置层级，如 ['a', 'b', 'c']
        """
        result = self.configuration
        for i in items:
            result = result[i]
        return result
