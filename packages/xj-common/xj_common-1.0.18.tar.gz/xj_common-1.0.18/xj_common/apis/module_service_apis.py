# encoding: utf-8
"""
@project: djangoModel->module_service_apis
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 模块开放服务注册
@created_time: 2023/6/5 9:28
"""
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.xj_module_service_services import XJModuleServiceServices
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper
from ..utils.user_wrapper import user_authentication_force_wrapper


class ModuleApiView(APIView):

    @api_view(["GET", "POST"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def services_list(self, *args, request_params, **kwargs):
        data, err = XJModuleServiceServices.services_list(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

