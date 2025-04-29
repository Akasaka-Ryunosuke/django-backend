from typing import Dict

from django.db import transaction
from .models import CodeInfo
from django.db.models import QuerySet
from django.db.models import Q


def create_code_info(data: Dict) -> CodeInfo:
    """
    创建一条 CodeInfo 记录
    """
    required_fields = ['user_id', 'question_id']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    try:
        with transaction.atomic():
            code_info = CodeInfo.objects.create(**data)
            return code_info
    except Exception as e:
        raise ValueError(f"Failed to create CodeInfo: {e}")


def delete_code_info(code_id: int) -> int:
    """
    删除 CodeInfo 记录
    :param code_id: 删除条件，例如 code_id=1
    :return: 删除的记录数
    """
    try:
        deleted_count, _ = CodeInfo.objects.filter(code_id=code_id).delete()
        return deleted_count
    except Exception as e:
        raise ValueError(f"Failed to delete CodeInfo: {e}")


def update_code_info(code_id: int, updates) -> CodeInfo:
    """
    更新 CodeInfo 记录
    :param code_id: 过滤条件必须确保更新对象的唯一
    :param updates: 更新字段，例如 {"score": 90, "run_time": 100}
    :return: 更新的记录
    """
    try:
        return CodeInfo.objects.filter(code_id=code_id).update(**updates)
    except Exception as e:
        raise ValueError(f"Failed to update CodeInfo: {e}")


def get_code_info(code_id: int) -> CodeInfo:
    """
    获取 CodeInfo 记录
    :param code_id: 根据 code_id 获取一条 CodeInfo 记录
    :return: 查询到的 CodeInfo 对象
    """
    try:
        code_info = CodeInfo.objects.get(code_id=code_id)
        return code_info
    except CodeInfo.DoesNotExist:
        raise ValueError(f"CodeInfo for user_id {code_id} does not exist")


def list_code_info(**kwargs) -> QuerySet:
    """
    根据多个条件查询 CodeInfo 记录
    :param kwargs: 查询条件，例如 user_id=1, question_id=2 等
    :return: QuerySet 对象
    """
    try:
        query = Q()
        for key, value in kwargs.items():
            if key == 'code_type' and isinstance(value, list):
                # 处理 type 多选（OR 条件）
                type_query = Q()
                for t in value:
                    type_query |= Q(code_type=t)
                query &= type_query
            else:
                # 其他条件（AND 条件）
                query &= Q(**{key: value})
        return CodeInfo.objects.filter(query)
    except Exception as e:
        raise ValueError(f"Failed to retrieve CodeInfo: {e}")
