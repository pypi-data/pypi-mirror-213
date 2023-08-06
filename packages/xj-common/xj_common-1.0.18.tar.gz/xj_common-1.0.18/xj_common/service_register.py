# encoding: utf-8
"""
@project: djangoModel->service_register
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 对外开放服务调用注册白名单
@created_time: 2023/1/12 14:29
"""

import xj_common
from .services import notice_services
from .utils.service_manager import ServiceManager

server_manager = ServiceManager()
data, err = server_manager.module_register(xj_common.module_info)


# ============= section 微服务测试放啊 start =========================
def hello(*args, name="word", **kwargs):
    """测试统一主次RPC方法注入"""
    return {"msg": "Hi " + str(name) + "!!!"}


# ============= section 微服务测试放啊 end =========================

# 对外服务白名单
register_list = [
    {
        "service_name": "hello",
        "io_mode": "OTHER",
        "data_type": "OTHER",
        "description": "测试统一注册RPC方法注入",
        "pointer": hello
    },
    {
        "service_name": "notice_add",
        "io_mode": "INSERT",
        "data_type": "MAIN",
        "description": "添加提醒",
        "pointer": notice_services.NoticeServices.notice_add
    },
    {
        "service_name": "notice_edit",
        "io_mode": "UPDATE",
        "data_type": "MAIN",
        "description": "提醒修改",
        "pointer": notice_services.NoticeServices.notice_edit
    }
]


# 遍历注册
def register():
    server_manager.register(register_list, xj_common)


if __name__ == '__main__':
    register()
