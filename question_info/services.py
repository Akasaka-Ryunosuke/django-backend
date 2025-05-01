from django.db import transaction
from django.db.models import QuerySet, Q

from .models import QuestionInfo

def create_question_info(question_id, question_raw=None, checkpoints_count=None):
    """
    创建一条 QuestionInfo 记录
    """
    try:
        with transaction.atomic():
            question_info = QuestionInfo.objects.create(
                question_id=question_id,
                question_raw=question_raw,
                checkpoints_count=checkpoints_count
            )
            return question_info
    except Exception as e:
        raise ValueError(f"Failed to create QuestionInfo: {e}")

def get_question_info(**kwargs):
    """
    根据多个条件查询 QuestionInfo 记录
    :param kwargs: 查询条件，例如 question_id="q1", checkpoints_count="5" 等
    :return: QuerySet 对象
    """
    try:
        return QuestionInfo.objects.filter(**kwargs)
    except Exception as e:
        raise ValueError(f"Failed to retrieve QuestionInfo: {e}")

def update_question_info(filters, updates):
    """
    更新 QuestionInfo 记录
    :param filters: 过滤条件，例如 {"question_id": "q1"}
    :param updates: 更新字段，例如 {"question_raw": "New question", "checkpoints_count": "8"}
    :return: 更新的记录数
    """
    try:
        return QuestionInfo.objects.filter(**filters).update(**updates)
    except Exception as e:
        raise ValueError(f"Failed to update QuestionInfo: {e}")

def delete_question_info(**kwargs):
    """
    删除 QuestionInfo 记录
    :param kwargs: 删除条件，例如 question_id="q1"
    :return: 删除的记录数
    """
    try:
        return QuestionInfo.objects.filter(**kwargs).delete()
    except Exception as e:
        raise ValueError(f"Failed to delete QuestionInfo: {e}")


def list_problem(**kwargs):
    try:
        query = Q()
        for key, value in kwargs.items():
            lookup_suffix = '__icontains'
            lookup = f"{key}{lookup_suffix}"
            query &= Q(**{lookup: value})

        results = QuestionInfo.objects.filter(query)

        enriched_results = []
        for q in results:
            first_line = q.question_raw.strip().splitlines()[0]
            if first_line.startswith('#'):
                problem_name = first_line.lstrip('#').strip()
            else:
                problem_name = '未知标题'
            enriched_results.append({
                'question_id': q.question_id,
                'question_name': problem_name,
            })

        return enriched_results

    except Exception as e:
        print(f"Error in list_problem query: {e}")
        raise ValueError(f"Failed to retrieve QuestionInfo records: {e}")