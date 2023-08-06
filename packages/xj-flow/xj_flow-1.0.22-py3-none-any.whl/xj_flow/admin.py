from django.contrib import admin

from .models import Flow, FlowNode, FlowAction, FlowNodeToAction, FlowActionToOperator, FlowNodeActionRule, FlowRecord, FlowApply


class FlowAdmin(admin.ModelAdmin):
    list_display = ('id', 'flow_name', 'module_name', 'description', "is_loop_flow", "must_execute_flows", "config")
    fields = ('id', 'flow_name', 'module_name', 'description', "is_loop_flow", "must_execute_flows", "config")
    search_fields = ('id', 'flow_name', 'module_name')
    readonly_fields = ['id']
    list_per_page = 20


class FlowToCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'flow', 'category_id',)
    fields = ('id', 'flow', 'category_id',)
    search_fields = ('id', 'flow', 'category_id',)
    readonly_fields = ['id']
    list_per_page = 20


class FlowNodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'flow_id', 'node_name', 'node_value', 'module_name', 'flow_number', 'status_code', 'summary', 'description', 'config', 'is_open_verify', "is_end_node")
    fields = ('id', 'flow_id', 'node_name', 'module_name', 'node_value', 'flow_number', 'status_code', 'summary', 'description', "config", 'is_open_verify', "is_end_node")
    search_fields = ('id', 'flow_id', 'node_name', 'module_name', 'summary')
    readonly_fields = ['id']
    ordering = ['flow_id', "flow_number"]
    list_per_page = 20


class FlowActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'name', 'description', 'config')
    fields = ('id', 'action', 'name', 'description', 'config')
    search_fields = ('id', 'action', 'name', 'description', 'config')
    readonly_fields = ['id']
    ordering = ['action']
    list_per_page = 20


class FlowNodeToActionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'flow_id', 'flow_node', 'flow_action', 'flow_to_node', "flow_to_fail_node", "ttl", 'role_list',
        'user_list', "is_automatic", "description", "is_using", "relate_data_key", "api"
    )
    fields = (
        'id', 'flow_id', 'flow_node', 'flow_action', 'flow_to_node', "flow_to_fail_node", "ttl", 'role_list',
        'user_list', "is_automatic", "description", "is_using", "relate_data_key", "api"
    )
    search_fields = ('id', 'flow_node__value', 'flow_action__action')
    readonly_fields = ['id', 'flow_id']
    ordering = ['flow_node__flow_id', 'flow_node__flow_number', 'flow_to_node']
    list_filter = ['flow_node__flow_id']

    def flow_id(self, item):
        return item.flow_node.flow_id

    flow_id.short_description = '流程ID'
    list_per_page = 20


class FlowActionToOperatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'flow_action_id', 'role_id', 'user_id')
    fields = ('id', 'flow_action_id', 'role_id', 'user_id')
    search_fields = ('id', 'flow_action_id', 'role_id', 'user_id')
    readonly_fields = ['id']
    list_per_page = 20


class FlowNodeActionRuleAdmin(admin.ModelAdmin):
    list_display = (
        "id", "flow_node_to_action", "rule_name", "rule_sort", "inflow_service", "inflow_module", "inflow_field", "outflow_module",
        "outflow_field", "default_value", "expression_string", "python_script", "is_using", "run_mode"
    )
    fields = (
        "id", "flow_node_to_action", "rule_name", "rule_sort", "inflow_service", "inflow_module", "inflow_field", "outflow_module",
        "outflow_field", "default_value", "expression_string", "python_script", "is_using", "run_mode"
    )
    search_fields = ('id', 'rule_name')
    readonly_fields = ['id']
    list_per_page = 20


class FlowRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user_id", "belong_role_id", "flow_node", "flow_action", "relate_data_key", "relate_data_value", "request_params", "process_context", "create_time"
    )
    fields = (
        "id", "user_id", "belong_role_id", "flow_node", "flow_action", "relate_data_key", "relate_data_value", "request_params", "process_context", "create_time"
    )
    search_fields = ('id', 'flow_node_id')
    readonly_fields = ['id', "create_time"]
    list_per_page = 20


class FlowApplyAdmin(admin.ModelAdmin):
    list_display = (
        "id", "apply_user_id", "apply_flow_node", "verify_user_id", "verify_role_id", "copy_to_users", "relate_data_key",
        "relate_data_value", "is_verified", "reply", "create_time", "update_time",
    )
    fields = (
        "id", "apply_user_id", "apply_flow_node", "verify_user_id", "verify_role_id", "copy_to_users", "relate_data_key",
        "relate_data_value", "is_verified", "reply", 'snapshot', "create_time", "update_time",
    )
    search_fields = ('id', 'flow_node')
    readonly_fields = ['id', "create_time", "update_time"]
    list_per_page = 20


admin.site.register(Flow, FlowAdmin)
admin.site.register(FlowNode, FlowNodeAdmin)
admin.site.register(FlowAction, FlowActionAdmin)
admin.site.register(FlowNodeToAction, FlowNodeToActionAdmin)
admin.site.register(FlowActionToOperator, FlowActionToOperatorAdmin)
admin.site.register(FlowNodeActionRule, FlowNodeActionRuleAdmin)
admin.site.register(FlowRecord, FlowRecordAdmin)
admin.site.register(FlowApply, FlowApplyAdmin)
