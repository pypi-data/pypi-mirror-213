"""HTTP服务"""
from eqmicro.client.http_service import http_server
from eqmicro.provider.provider_mgt import ProviderMGT
from eqmicro.components.ext_lib import not_contain_key
import os
from threading import Thread


class MyHttp:

    def __init__(self, configuration):
        self.http_conf = configuration
        if not_contain_key(self.http_conf, 'port') is True:
            self.http_conf['port'] = 9702

        # 判断服务信息中是否含有services字段，即服务列表路径。没有的话赋予一个初始值
        if not_contain_key(self.http_conf, 'services') is True:
            self.http_conf['services'] = os.path.abspath(os.path.join(os.getcwd(), "../gateway"))
        self.provider_mgt = ProviderMGT(self.http_conf['services'])

    def __http_server__(self):
        """
        供WEB访问的HTTP服务启动
        """
        http_server(self.http_conf, self.provider_mgt.services_class).serve_forever()

    def start(self):
        Thread(target=self.__http_server__).start()
