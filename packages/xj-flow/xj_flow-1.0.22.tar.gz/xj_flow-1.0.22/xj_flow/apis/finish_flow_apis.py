# encoding: utf-8
"""
@project: djangoModel->finish_flow_apis
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户完成流程相关的API
@created_time: 2023/6/13 9:43
"""
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.flow_finish_flows import FlowFinishFlowsService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper, flow_service_wrapper
from ..utils.user_wrapper import user_authentication_force_wrapper


class FinishFlowsAPIView(APIView):
    @request_params_wrapper
    def finish_flow_list(self, *args, request_params, **kwargs):
        need_pagination = request_params.get("need_pagination")
        only_first = request_params.get("only_first")
        data, err = FlowFinishFlowsService.get_finish_flows(
            params=request_params,
            need_pagination=need_pagination,
            only_first=only_first
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["POST", "PUT"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    @flow_service_wrapper
    def finish_flow_add(self, *args, request_params, user_info, **kwargs):
        flow_id = request_params.get("flow_id")
        user_id = request_params.get("user_id", user_info.get("user_id"))
        data, err = FlowFinishFlowsService.add_finish_flows(
            flow_id=flow_id,
            user_id=user_id
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @user_authentication_force_wrapper
    @request_params_wrapper
    @flow_service_wrapper
    def finish_flow_rebut(self, *args, request_params, user_info, **kwargs):
        flow_id = request_params.get("flow_id")
        user_id = request_params.get("user_id", user_info.get("user_id"))
        data, err = FlowFinishFlowsService.rebut_finish_flows(user_id=user_id, flow_id=flow_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
