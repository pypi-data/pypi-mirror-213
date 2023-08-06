# encoding: utf-8
"""
@project: djangoModel->flow_verify_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 流程审批服务
@created_time: 2023/5/31 10:42
"""
from django.core.paginator import EmptyPage, Paginator
from django.db.models import F

from ..models import FlowApply, FlowNode, FlowNodeToAction, Flow
from ..utils.custom_tool import force_transform_type, format_params_handle, filter_fields_handler, dynamic_load_class
from ..utils.join_list import JoinList


class FlowApplyService(object):
    """流程审批服务"""

    @staticmethod
    def __node_value_to_id(node_value):
        if not node_value:
            return None
        flow_node_map = FlowNode.objects.filter(node_value=node_value).values("id").first() or {}
        flow_node_id, is_pass = force_transform_type(variable=flow_node_map.get("id", None), var_type="int", default=None)
        return flow_node_id

    @staticmethod
    def get_flow_apply(params: dict = None, need_pagination=True, only_first=False, **kwargs):
        """
        查询流程审批
        :param only_first: 查询单挑记录是否存在
        :param need_pagination: 是否需要分页
        :param params: 查询参数
        :return: data, err
        """
        # ----------------- section 参数类型校验 start ------------------------
        params, is_pass = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, is_pass = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)
        # 查询模式
        need_pagination, is_pass = force_transform_type(variable=need_pagination, var_type="bool", default=True)
        only_first, is_pass = force_transform_type(variable=only_first, var_type="bool", default=False)
        # 分页
        page, is_pass = force_transform_type(variable=params.pop("page", 1), var_type="int", default=1)
        size, is_pass = force_transform_type(variable=params.pop("page", 10), var_type="int", default=10)
        # 排序
        sort = str(params.get("sort"))
        sort = sort if sort in ["id", "-id", "create_time", "update_time", "-create_time", "-update_time"] else "-update_time"
        # ----------------- section 参数类型校验 end   ------------------------

        # ----------------- section 节点value转id start ------------------------
        apply_flow_node_id = FlowApplyService.__node_value_to_id(params.get("apply_flow_node_value"))
        if apply_flow_node_id:
            params.setdefault("apply_flow_node_id", apply_flow_node_id)
        # ----------------- section 节点value转id end   ------------------------

        # ----------------- section 字段过滤 start ------------------------
        filter_fields = filter_fields_handler(
            input_field_expression=params.pop("filter_fields", None),
            all_field_list=[
                "id", "flow_id", "apply_user_id", "apply_flow_node_id", "verify_user_id", "verify_role_id", "copy_to_users",
                "relate_data_key", "relate_data_value", "is_verified", "reply", "create_time", "update_time",
                "apply_flow_node_summary", "apply_flow_node_config", "snapshot"
            ]
        )
        params = format_params_handle(
            param_dict=params,
            is_remove_empty=True,
            filter_filed_list=[
                "id|int", "apply_user_id|int", "apply_flow_node_id|int", "verify_user_id|int", "verify_role_id|int",
                "relate_data_key", "relate_data_value", "is_verified|int", "flow_id|int", "flow_id_list|list_int",
                "create_time_start|date", "update_time_start|date", "create_time_end|date", "update_time_end|date"
            ],
            alias_dict={
                "create_time_start": "create_time__gte", "create_time_end": "create_time__lte",
                "update_time_start": "update_time__gte", "update_time_end": "update_time__lte",
                "flow_id_list": "flow_id__in"
            },
            split_list=["flow_id_list"]
        )

        # 默认查看未审批完成的审理流程
        params.setdefault('is_verified', 0)
        # ----------------- section 字段过滤 end   ------------------------

        # ----------------- section 构建ORM start ------------------------
        flow_obj = FlowApply.objects.annotate(
            apply_flow_node_value=F("apply_flow_node__node_value"),
            apply_flow_node_name=F("apply_flow_node__node_name"),
            apply_flow_node_config=F("apply_flow_node__config"),
            apply_flow_node_summary=F("apply_flow_node__summary"),
            apply_flow_node_status_code=F("apply_flow_node__status_code"),
            flow_id=F("apply_flow_node__flow_id"),
        ).filter(**params).order_by(sort).values(*filter_fields)
        total = flow_obj.count()
        # ----------------- section 构建ORM end   ------------------------

        # ----------------- section 分情况查询 start ------------------------
        is_not_pagination = not need_pagination and total <= 50
        if only_first:  # 查询用户是否提交了审批
            return True if flow_obj.first() else False, None
        elif is_not_pagination:  # 列表显示
            finish_list = flow_obj.to_json()
        else:  # 分页查询
            paginator = Paginator(flow_obj, size)
            try:
                page_obj = paginator.page(page)
            except EmptyPage:
                return {"page": page, "size": size, "total": total, "list": []}, None
            finish_list = list(page_obj.object_list)
        # ----------------- section 分情况查询 end   ------------------------

        # ----------------- section 动作列表拼接 start -----------------------
        # 获取节点动作列表
        apply_flow_node_list = [i["apply_flow_node_id"] for i in finish_list]
        node_to_action_list = FlowNodeToAction.objects.annotate(
            flow_action_name=F("flow_action__name"),
            flow_action_value=F("flow_action__action"),
            flow_action_config=F("flow_action__config")
        ).filter(flow_node_id__in=apply_flow_node_list).values(
            "flow_node_id", "flow_action_id", "flow_action_name", "flow_action_value", "flow_action_config"
        )

        # 建立节点对动作映射
        node_to_action_map = {}
        for i in node_to_action_list:
            flow_node_id = i.pop("flow_node_id", None)
            if node_to_action_map.get(flow_node_id):
                node_to_action_map[flow_node_id].append(i)
            else:
                node_to_action_map[flow_node_id] = [i]

        # 结果补全流程动作信息
        for j in finish_list:
            j["flow_action_list"] = node_to_action_map.get(j["apply_flow_node_id"], [])
        # ----------------- section 动作列表拼接 end   ------------------------
        # note 如果没有传递流程ID，则仅仅返回审批信息
        if not params.get("flow_id"):
            return finish_list if is_not_pagination else {"page": page, "size": size, "total": total, "list": finish_list}, None

        # ----------------- section 获取审批信息 start ------------------------
        # note 如果指定某个分批类，则可以看到审批联动信息
        try:
            # 获取审批绑定服务
            config_obj = Flow.objects.filter(id=params.get("flow_id")).values("id", "config").first()
            flow_config = config_obj.get("config")
            assert flow_config

            # 发现服务及配置
            module = flow_config.get("action", {}).get("get_apply_info", {}).get("module")
            service = flow_config.get("action", {}).get("get_apply_info", {}).get("service")
            relate_data_values_key = flow_config.get("action", {}).get("get_apply_info", {}).get("relate_data_values_key")
            splice_values_key = flow_config.get("action", {}).get("get_apply_info", {}).get("splice_values_key", "id")
            service, err = dynamic_load_class(import_path=module, class_name=service)
            assert not err

            # 调用服务，或者审批数据
            call_params = {relate_data_values_key: [i["relate_data_value"] for i in finish_list]}
            data, err = service(**call_params)
            assert not err

            # 拼接数据
            JoinList(finish_list, data, l_key="relate_data_value", r_key=splice_values_key).join()
        except Exception as e:
            pass

        return finish_list if is_not_pagination else {"page": page, "size": size, "total": total, "list": finish_list}, None
        # ----------------- section 获取审批信息 end   ------------------------

    @staticmethod
    def add_flow_apply(params: dict = None, **kwargs):
        """
        添加流程审批
        :param params: 查询参数
        :return: data, err
        """
        # ----------------- section 参数类型校验 start ------------------------
        params, is_pass = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, is_pass = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)
        # ----------------- section 参数类型校验 end   ------------------------

        # value转换为ID
        apply_flow_node_id = FlowApplyService.__node_value_to_id(params.get("apply_flow_node_value"))
        params.setdefault("apply_flow_node_id", apply_flow_node_id)
        request_params = params
        # ----------------- section 字段过滤 start ------------------------
        try:
            # 根据配置的关联数据key自动补全数据
            if params.get("relate_data_key"):
                params.setdefault("relate_data_value", params.get(params.get("relate_data_key", "")))
            # 过滤
            params = format_params_handle(
                param_dict=params,
                is_remove_empty=True,
                is_validate_type=True,
                filter_filed_list=[
                    "id|int", "apply_user_id|int", "user_id|int", "apply_flow_node_id|int", "verify_user_id|int", "verify_role_id|int",
                    "copy_to_users|list_int", "relate_data_key", "relate_data_value", "is_verified|int"
                ],
                alias_dict={"user_id": "apply_user_id"}
            )
            # 必填性验证
            must_keys = ["apply_user_id", "apply_flow_node_id", "relate_data_key", "relate_data_value"]
            for i in must_keys:
                if not params.get(i):
                    return None, i + "必填"
            params.setdefault("is_verified", 0)
        except ValueError as e:
            return None, str(e)
        # ----------------- section 字段过滤 end   ------------------------

        # ----------------- section 判断节点是否支持审批 start ------------------------
        is_open_verify = FlowNode.objects.filter(id=params.get("apply_flow_node_id")).values("is_open_verify").first()
        if not is_open_verify or not is_open_verify.get("is_open_verify"):
            return None, "该节点不支持创建流程审批"
        # ----------------- section 判断节点是否支持审批 end   ------------------------

        # ----------------- section 构建ORM start ------------------------
        verify_obj = FlowApply.objects.filter(
            apply_user_id=params.get("apply_user_id"),
            apply_flow_node_id=params.get("apply_flow_node_id"),
            is_verified=0
        ).first()

        if verify_obj:
            return None, "审批已存在无需重复创建"

        params["snapshot"], is_pass = force_transform_type(variable=request_params, var_type="dict", default={})
        verify_obj = FlowApply(**params)
        verify_obj.save()
        return None, None
        # ----------------- section 构建ORM end   ------------------------

    @staticmethod
    def edit_flow_apply(pk: int = None, params: dict = None, **kwargs):
        """
        编辑流程审批
        :param params: 编辑参数
        :param pk: 修改主键
        :return: data, err
        """
        # ----------------- section 参数类型校验 start -------------------
        params, is_pass = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, is_pass = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)
        pk, is_pass = force_transform_type(variable=params.get("pk", params.get("id", pk)), var_type="int")
        apply_user_id, is_pass = force_transform_type(variable=params.get("apply_user_id", params.get("user_id", pk)), var_type="int")
        # ----------------- section 参数类型校验 end   -------------------

        # ----------------- section 流程value转换为流程ID start -------------------
        # 因为再数据迁移过程中ID会发生变化，但是value不会变
        apply_flow_node_id = FlowApplyService.__node_value_to_id(params.get("apply_flow_node_value"))
        params.setdefault("apply_flow_node_id", apply_flow_node_id)
        search_apply_node_id = FlowApplyService.__node_value_to_id(params.pop("search_apply_node_value", None))
        # ----------------- section 流程value转换为流程ID end   -------------------

        # ----------------- section 字段过滤 start -----------------------
        try:
            params = format_params_handle(
                param_dict=params,
                is_remove_empty=True,
                is_validate_type=True,
                filter_filed_list=[
                    "apply_flow_node_id|int",
                    "verify_user_id|int",
                    "verify_role_id|int",
                    "copy_to_users|list_int",
                    "is_verified|int",
                    "relate_data_key",
                    "relate_data_value",
                    "reply",
                ]
            )
        except ValueError as e:
            return None, str(e)
        if not params:
            return None, "没有修改项"
        # ----------------- section 字段过滤 end   -----------------------

        # ----------------- section 构建ORM start ------------------------
        if pk:
            verify_obj = FlowApply.objects.filter(id=pk, is_verified=0)
            if not verify_obj:
                return None, "审批不存在"
        elif apply_user_id and search_apply_node_id:
            verify_obj = FlowApply.objects.filter(apply_user_id=apply_user_id, apply_flow_node_id=search_apply_node_id, is_verified=0)
        else:
            return None, "参数错误，无法定位到有效的的审批"
        if not verify_obj.first():
            return None, "没有找到你要找的审批"
        # 审批修改
        verify_obj.update(**params)
        return None, None
        # ----------------- section 构建ORM end   ------------------------
