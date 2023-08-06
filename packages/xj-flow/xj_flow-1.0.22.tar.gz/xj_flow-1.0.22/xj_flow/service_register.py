# encoding: utf-8
"""
@project: djangoModel->service_register
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 对外开放服务调用注册白名单
@created_time: 2023/1/12 14:29
"""

import xj_flow
from .services import flow_apply_service
from .utils.service_manager import ServiceManager

# 对外服务白名单
register_list = [
    {
        "service_name": "add_flow_apply",
        "pointer": flow_apply_service.FlowApplyService.add_flow_apply
    },
    {
        "service_name": "edit_flow_apply",
        "pointer": flow_apply_service.FlowApplyService.edit_flow_apply
    },
]

server_manager = ServiceManager()


# 遍历注册
def register():
    for i in register_list:
        setattr(xj_flow, i["service_name"], i["pointer"])
        server_manager.put_service(route=i["service_name"], method=i["pointer"])


if __name__ == '__main__':
    register()
