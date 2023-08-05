"""
基于http.server的简单服务器对象
"""

import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from socket import gethostbyname, gethostname
import json
from eqmicro.components.ext_lib import not_contain_key
import cgi


def preset_get_params(request):
    """
    GET 参数列表格式化
    :param request: GET请求链接
    :return: service_path 服务地址, params 参数列表
    """
    service_path = []
    params = {}
    try:
        # ? 分割请求地址和请求参数
        path_params = request.split('?')
        # 请求地址使用 / 分割
        service_path = path_params[0][1:].split('/')
        # 请求参数使用 & 分割
        params_item = path_params[1].split('&')
        # a=b 格式的请求参数转换成 dict 形式
        for item in params_item:
            key_value = item.split('=')
            params[key_value[0]] = key_value[1]
    except Exception as e:
        print('[eqmicro] [GET请求] 参数格式化失败', e)
        print(traceback.format_exc())
    return service_path, params


def func_exec(service_list, service_path, params):
    """
    函数执行
    :param service_list: 服务列表
    :param service_path: 请求的服务方法的路径 list 如 a/b/c ['a','b','c']
    :param params: 请求服务方法的入参
    """
    try:
        # 循环遍历加载的服务路径，获取可执行的函数
        for i in service_path[:-1]:
            service_list = service_list[i]
        method = getattr(service_list['func'], service_path[-1])
        # 执行结果作为响应数据
        response = method(**params)
    except Exception as e:
        print('[eqmicro] [函数执行失败]', e)
        print(traceback.format_exc())
        response = 'Function execution failed! Details: ' + str(e)
    return response


class MyHttpServer(BaseHTTPRequestHandler):
    my_server_list = {}
    server_version = "Eqmicro"
    sys_version = 'Python/3'

    def do_GET(self):
        """
        处理GET请求
        :return: http response
        """
        path = self.path
        # 请求参数格式化
        service_path, params = preset_get_params(path)
        # 执行请求的方法
        res = func_exec(self.my_server_list, service_path, params)
        self.send_response(200)
        # accept 含有 image，认为是图片文件读取
        if self.headers['accept'].__contains__('image'):
            # 先默认返回 image/jpeg 文件
            self.send_header("Content-type", "image/jpeg")
        else:
            self.send_header("Content-type", "application/json")
            res = json.dumps(res).encode()
        self.end_headers()
        self.wfile.write(res)

    def do_POST(self):
        """
        处理POST请求
        :return: http response
        """
        print('\r\n请求头', self.headers)
        # 请求数据
        request_data = None
        # 请求内容类型
        content_type = self.headers['content-type']
        if content_type.__contains__('application/json'):
            # 请求参数为json类型，对请求参数进行json格式化
            req_data = self.rfile.read(int(self.headers['content-length']))
            request_data = json.loads(req_data)
        elif content_type.__contains__('multipart/form-data') and content_type.__contains__('boundary'):
            # 请求参数是文件类型，读取文件到cgi中
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']})
            request_data = {'form_data': form}
        # 请求路径，根据 / 进行分割
        path = self.path
        service_path = path[1:].split('/')
        # 执行请求的函数
        res = func_exec(self.my_server_list, service_path, request_data)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(res).encode())


def http_server(server_conf, server_list):
    """
    实例化http服务器对象
    :param server_conf: http服务器配置
    :param server_list: http服务列表
    :return: http服务器对象
    """
    host = gethostbyname(gethostname()) if not_contain_key(server_conf, 'host') else server_conf['host']
    mhs = MyHttpServer
    mhs.my_server_list = server_list
    print(f"[eqmicro] HTTP Server starting on {host}:{server_conf['port']}")
    server = HTTPServer((host, int(server_conf['port'])), mhs)
    return server


def main():
    hs = http_server({'port': 9701}, {'test_service': {'func': TestCommon()}})
    hs.serve_forever()


class TestCommon:
    """
    用于测试服务，实现
    """
    name = 'eqmicro'
    age = '2'

    def hello(self, name):
        return 'Hi,' + name + '! I\'m ' + self.name + ', ' + self.age + ' years old.'

    def upload(self, form_data):
        print(self.name, '[文件上传参数]', form_data.keys())
        for field in form_data.keys():
            field_item = form_data[field]
            if field_item.filename is None:
                print(self.name, '[文件名不存在] 为非文件类入参 [ key:', field, ', value:', field_item.value, ']')
                continue
            file_name = 'D:/downloads/' + field_item.filename
            file_value = field_item.value
            file_size = len(file_value)
            with open(file_name, 'wb') as f:
                f.write(file_value)
            print(self.name, '[文件b保存成功] 文件大小:', file_size, '文件尺寸:', file_name)
        return 'success'

    def download(self, file_path):
        print(self.name, '[要下载的文件]', file_path)
        file = open(file_path, "rb")
        file_data = file.read()
        return file_data


if __name__ == '__main__':
    main()
