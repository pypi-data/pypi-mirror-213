# encoding: utf-8
"""
@project: djangoModel->module_services
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 模块服务
@created_time: 2023/6/2 17:59
"""
from django.core.paginator import Paginator, EmptyPage

from ..models import Modules
from ..utils.custom_tool import format_params_handle, force_transform_type


class XJModuleServices(object):
    @staticmethod
    def init_modules():
        """初始化数据表"""
        try:
            Modules.truncate()
        except Exception as e:
            return None, str(e)
        return None, None

    @staticmethod
    def module_register(params: str = None, **kwargs):
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
            filter_filed_list=["module_name", "module_type", "description"],
        )
        must_keys = ["module_name", "module_type"]
        for i in must_keys:
            if not filter_params.get(i):
                return None, str(i) + "不可以为空"

        # 构建ORM
        try:
            orm_obj = Modules(**filter_params)
            orm_obj.save()
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None

    @staticmethod
    def module_list(params: dict = None, need_pagination: int = 0, **kwargs):
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
            filter_filed_list=["module_name", "module_type"]
        )
        module_obj = Modules.objects.extra(select={
            'created_time': 'DATE_FORMAT(created_time, "%%Y-%%m-%%d %%H:%%i:%%s")'
        }).filter(**params).values("id", "module_name", "module_type", "description", "created_time")
        total = module_obj.count()

        # 不许分页直接返回
        if not need_pagination and total <= 200:
            notice_type_list = list(module_obj)
            return notice_type_list, None

        paginator = Paginator(module_obj, size)
        try:
            module_obj = paginator.page(page)
        except EmptyPage:
            return {"page": int(page), "size": int(size), "total": total, "list": []}
        except Exception as e:
            return None, f'{str(e)}'

        return {"page": int(page), "size": int(size), "total": total, "list": list(module_obj.object_list)}, None
