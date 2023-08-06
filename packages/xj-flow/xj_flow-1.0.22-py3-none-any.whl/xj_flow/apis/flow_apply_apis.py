# encoding: utf-8
"""
@project: djangoModel->flow_verify_apis
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 流程审批功能接口
@created_time: 2023/5/31 13:23
"""
from rest_framework.views import APIView

from ..services.flow_apply_service import FlowApplyService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper, flow_service_wrapper
from ..utils.user_wrapper import user_authentication_force_wrapper


class FlowApplyAPIView(APIView):
    @request_params_wrapper
    def apply_list(self, *args, request_params, **kwargs):
        need_pagination = request_params.get("need_pagination")
        is_has = request_params.get("is_has")
        data, err = FlowApplyService.get_flow_apply(params=request_params, need_pagination=need_pagination, only_first=is_has)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @user_authentication_force_wrapper
    @request_params_wrapper
    @flow_service_wrapper
    def apply_add(self, *args, request_params, user_info, **kwargs):
        request_params.setdefault("apply_user_id", user_info.get("user_id"))
        request_params.setdefault("user_id", user_info.get("user_id"))
        data, err = FlowApplyService.add_flow_apply(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @user_authentication_force_wrapper
    @request_params_wrapper
    @flow_service_wrapper
    def apply_edit(self, *args, request_params, user_info, **kwargs):
        pk = request_params.get("pk") or request_params.get("id") or kwargs.get("pk", None)
        data, err = FlowApplyService.edit_flow_apply(pk=pk, params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
