# _*_coding:utf-8_*_
from django.conf.urls import url

from .apis.finish_flow_apis import FinishFlowsAPIView
from .apis.flow_action_list import FlowActionList
from .apis.flow_apply_apis import FlowApplyAPIView
from .apis.flow_list import FlowList
from .apis.flow_node_list import FlowNodeList
from .apis.flow_node_rule_list import FlowNodeActionRuleList
from .apis.flow_node_to_action_list import FlowNodeToActionList
from .apis.flow_process import FlowProcess
from .service_register import register

# 应用名称
app_name = 'xj_flow'

register()
urlpatterns = [
    url(r'^list/?$', FlowList.as_view(), name='flow_list'),
    url(r'^node_list/?$', FlowNodeList.as_view(), name='flow_node_list'),
    url(r'^action_list/?$', FlowActionList.as_view(), name='flow_action_list'),
    url(r'^node_to_action_list/?$', FlowNodeToActionList.as_view(), name='flow_node_to_action_list'),
    url(r'^node_action_rule_list/?$', FlowNodeActionRuleList.as_view(), name='flow_node_action_rule_list'),
    url(r'^process/?$', FlowProcess.as_view(), name='flow_process'),

    # 流程审批相关API
    url(r'^verify_list/?$', FlowApplyAPIView.apply_list, name='verify_list'),
    url(r'^verify_add/?$', FlowApplyAPIView.apply_add, name='verify_add'),
    url(r'^verify_edit/?$', FlowApplyAPIView.apply_edit, name='verify_edit'),

    # 用户完成流程相关
    url(r'^finish_flows/?$', FinishFlowsAPIView.finish_flow_list, name='finish_flow_list'),
    url(r'^finish_flow_add/?$', FinishFlowsAPIView.finish_flow_add, name='finish_flow_add'),
    url(r'^finish_flow_rebut/?$', FinishFlowsAPIView.finish_flow_rebut, name='finish_flow_edit'),
]
