"""
协议类型定义
register - 注册中心相关
provider - 服务提供者相关
consumer - 消费者相关
"""
protocol_number_list = {
    'register': {
        'change': '服务变更通知，由register发送给consumer',
        'check': '服务状态检查，由register发送给provider'
    },
    'provider': {
        'service': '',
        'register': '服务注册，由provider发送给register',
        'health': '服务状态同步，由provider发送给register'
    },
    'consumer': {
        'pull': '服务拉取，从注册中心获取活跃的服务，由consumer发送给register',
        'call': '远程服务调用，由consumer发送给provider',
        'invalid': 'consumer调用provider失败，同步结果给注册中心，由consumer发送给register'
    }
}


def init_protocol(option='req'):
    """
    新的协议
    """
    protocol = {
        'header': {
            'protocol': {
                'type': '',
                'name': ''
            },
            'option': option
        },
        'body': {
            'code': '',  # success-正常，error-失败，warning-警告
            'message': '',
            'data': ''
        }
    }

    return protocol
