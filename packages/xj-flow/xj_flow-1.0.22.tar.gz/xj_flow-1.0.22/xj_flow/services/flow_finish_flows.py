# encoding: utf-8
"""
@project: djangoModel->flow_finish_flows
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户完成流程
@created_time: 2023/6/12 9:18
"""
from django.core.paginator import Paginator, EmptyPage

from ..models import FlowFinishFlow
from ..utils.custom_tool import force_transform_type, format_params_handle


class FlowFinishFlowsService(object):
    @staticmethod
    def add_finish_flows(flow_id: int = None, user_id: int = None, **kwargs):
        """完成流程"""
        flow_id, err = force_transform_type(variable=flow_id, var_type="int")
        user_id, err = force_transform_type(variable=user_id, var_type="int")
        if not user_id or not flow_id:
            return None, "参数错误"
        has_flow = FlowFinishFlow.objects.filter(flow_id=flow_id, user_id=user_id, is_rebut=0).first()
        if not has_flow:
            flow_obj = FlowFinishFlow(
                flow_id=flow_id,
                user_id=user_id
            )
            flow_obj.save()
        return None, None

    @staticmethod
    def rebut_finish_flows(user_id: int = None, flow_id: int = None, flow_id_list: list = None, **kwargs):
        """驳回流程"""
        try:
            if flow_id:
                FlowFinishFlow.objects.filter(flow_id=flow_id, user_id=user_id, is_rebut=0).update(is_rebut=1)
            if flow_id_list:
                FlowFinishFlow.objects.filter(flow_id__in=flow_id_list, user_id=user_id, is_rebut=0).first()
        except Exception as e:
            return None, "msg:" + str(e).replace(";", " ").replace(":", " ") + ";" + "tip:添加失败，请稍后再试"

        return None, None

    @staticmethod
    def get_finish_flows(params: dict = None, need_pagination: bool = True, only_first: bool = None, **kwargs):
        """查询用户的完成流程"""
        # -------------------- section 参数过滤 start ----------------------------------
        params, err = force_transform_type(variable=params, var_type="dict", default={})
        kwargs, err = force_transform_type(variable=kwargs, var_type="dict", default={})
        params.update(kwargs)
        page, err = force_transform_type(variable=params.get("page"), var_type="int", default=1)
        size, err = force_transform_type(variable=params.get("size"), var_type="int", default=10)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["user_id|int", "flow_id|int", "is_rebut|int", "flow_id_list|list_int"],
            alias_dict={"flow_id_list": "flow_id__in"}
        )
        # -------------------- section 参数过滤 end    ----------------------------------

        # -------------------- section 构建ORM start ----------------------------------
        flows_obj = FlowFinishFlow.objects.filter(**params).values()
        total = flows_obj.count()
        if only_first:  # 查询用户是否提交了审批
            return True if flows_obj.first() else False, None
        elif not need_pagination and total <= 500:  # 列表显示
            finish_list = list(flows_obj)
            return finish_list, None
        else:  # 分页查询
            paginator = Paginator(flows_obj, size)
            try:
                page_obj = paginator.page(page)
            except EmptyPage:
                return {"page": page, "size": size, "total": total, "list": []}, None
            finish_list = list(page_obj.object_list)
        return {"page": page, "size": size, "total": total, "list": finish_list}, None
        # -------------------- section 构建ORM end   ----------------------------------
