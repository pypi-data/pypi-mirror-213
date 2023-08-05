"""
定义服务返回信息列表
"""


class Res:
    """
    支持响应自定义
    """

    def __init__(self, code_list=None):
        """
        初始化
        :param code_list: 自定义的响应码与响应信息列表
        """
        self.code_list = {
            'default': 'None',
            '2000': 'Success',
            '4000': 'Not Found',
            '5000': 'Error'
        }
        if code_list is not None and type(code_list) == 'dict':
            self.code_list.update(code_list)

    def res(self, code=None, message=None, data=None):
        """
        响应处理
        :param code: 响应码
        :param message: 响应描述
        :param data: 响应体
        :return: 响应信息
        """
        if code is None:
            code = 'default'
        if message is None:
            message = self.code_list[code]
        return {
            'code': code,
            'message': message,
            'data': data
        }

    def success(self, data=None):
        return {
            'code': '2000',
            'message': self.code_list['2000'],
            'data': data
        }

    def not_found(self, data=None):
        return {
            'code': '4000',
            'message': self.code_list['4000'],
            'data': data
        }

    def error(self, data=None):
        return {
            'code': '5000',
            'message': self.code_list['5000'],
            'data': data
        }
