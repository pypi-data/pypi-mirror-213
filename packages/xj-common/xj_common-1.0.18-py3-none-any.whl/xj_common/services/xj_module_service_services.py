# encoding: utf-8
"""
@project: djangoModel->open_service_seervices
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 系统服务
@created_time: 2023/6/5 9:30
"""
from django.core.paginator import Paginator, EmptyPage

from ..models import ModuleServices
from ..utils.custom_tool import force_transform_type, format_params_handle


class XJModuleServiceServices(object):
    @staticmethod
    def init_services():
        """初始化数据表"""
        try:
            ModuleServices.truncate()
        except Exception as e:
            return None, str(e)
        return None, None

    @staticmethod
    def services_register(params: str = None, **kwargs):
        """
        模块注册
        :param params: 参数
        :param kwargs: 聚名参数
        :return: data,err
        """
        params, is_pass = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, is_pass = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)

        # 需要修改的字段过滤
        filter_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["module_name", "service_name", "description", "io_mode", "data_type"],
        )
        must_keys = ["module_name", "service_name", "io_mode", "data_type"]
        for i in must_keys:
            if not filter_params.get(i):
                return None, str(i) + "不可以为空"

        # 构建ORM
        try:
            orm_obj = ModuleServices(**filter_params)
            orm_obj.save()
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None

    @staticmethod
    def services_list(params: dict = None, need_pagination: int = 0, **kwargs):
        """
        模块列表
        :param params:
        :param need_pagination:
        :param kwargs:
        :return:
        """
        params, is_pass = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, is_pass = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)

        page, is_pass = force_transform_type(variable=params.pop("page", 1), var_type="int", default=1)
        size, is_pass = force_transform_type(variable=params.pop("size", 10), var_type="int", default=10)
        if size > 200:
            return None, "分页不可以超过200"

        # 参数过滤
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["module_name", "service_name", "io_mode", "data_type"]
        )
        services_obj = ModuleServices.objects.extra(select={
            'created_time': 'DATE_FORMAT(created_time, "%%Y-%%m-%%d %%H:%%i:%%s")'
        }).filter(**params).values(
            "id", "module_name", "service_name", "description", "io_mode", "data_type", "created_time"
        )
        total = services_obj.count()

        # 不许分页直接返回
        if not need_pagination and total <= 200:
            notice_type_list = list(services_obj)
            return notice_type_list, None

        paginator = Paginator(services_obj, size)
        try:
            services_obj = paginator.page(page)
        except EmptyPage:
            return {"page": int(page), "size": int(size), "total": total, "list": []}
        except Exception as e:
            return None, f'{str(e)}'

        return {"page": int(page), "size": int(size), "total": total, "list": list(services_obj.object_list)}, None
