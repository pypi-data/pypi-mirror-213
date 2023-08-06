# encoding: utf-8
"""
@project: djangoModel->modules_apis
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 系统模块API
@created_time: 2023/6/5 9:26
"""
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.xj_module_services import XJModuleServices
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper
from ..utils.user_wrapper import user_authentication_force_wrapper


class ModuleApiView(APIView):
    @api_view(["POST"])
    @user_authentication_force_wrapper
    def init_modules(self, *args, **kwargs):
        data, err = XJModuleServices.init_modules()
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["PUT", "POST"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def module_register(self, *args, request_params, **kwargs):
        data, err = XJModuleServices.module_register(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["GET", "POST"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def module_list(self, *args, request_params, **kwargs):
        data, err = XJModuleServices.module_list(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
