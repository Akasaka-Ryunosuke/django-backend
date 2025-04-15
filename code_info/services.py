from django.db import transaction
from .models import CodeInfo

def create_code_info(user_id=None, question_id=None, code_raw=None, code_type=None, score=None, run_time=None, upload_time=None):
    """
    创建一条 CodeInfo 记录
    """
    try:
        with transaction.atomic():
            code_info = CodeInfo.objects.create(
                user_id=user_id,
                question_id=question_id,
                code_raw=code_raw,
                code_type=code_type,
                score=score,
                run_time=run_time,
                upload_time=upload_time
            )
            return code_info
    except Exception as e:
        raise ValueError(f"Failed to create CodeInfo: {e}")

def get_code_info(**kwargs):
    """
    根据多个条件查询 CodeInfo 记录
    :param kwargs: 查询条件，例如 user_id=1, question_id=2 等
    :return: QuerySet 对象
    """
    try:
        return CodeInfo.objects.filter(**kwargs)
    except Exception as e:
        raise ValueError(f"Failed to retrieve CodeInfo: {e}")

def update_code_info(filters, updates):
    """
    更新 CodeInfo 记录
    :param filters: 过滤条件，例如 {"user_id": 1, "question_id": 2}
    :param updates: 更新字段，例如 {"score": 90, "run_time": 100}
    :return: 更新的记录数
    """
    try:
        return CodeInfo.objects.filter(**filters).update(**updates)
    except Exception as e:
        raise ValueError(f"Failed to update CodeInfo: {e}")

def delete_code_info(**kwargs):
    """
    删除 CodeInfo 记录
    :param kwargs: 删除条件，例如 user_id=1, question_id=2
    :return: 删除的记录数
    """
    try:
        return CodeInfo.objects.filter(**kwargs).delete()
    except Exception as e:
        raise ValueError(f"Failed to delete CodeInfo: {e}")