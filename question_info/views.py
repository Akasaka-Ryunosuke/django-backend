import json

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tmp.models import QuestionInfo
from utils.code_test.code_test import submit_code
from utils.enums import StatusCodeEnum
from utils.exceptions import GlobalException
from utils.paginator import MyPaginator
from utils.result import ok
from .services import create_question_info, get_question_info, update_question_info, delete_question_info, list_problem


@csrf_exempt
def question_info_create(request):
    """
    创建 QuestionInfo 记录
    """
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            question_id = payload.get("question_id")
            question_raw = payload.get("question_raw")
            question_info = create_question_info(
                question_id=question_id,
                question_raw=question_raw,
                checkpoints_count=None
            )
            return ok(str(question_info))
        except Exception as e:
            raise GlobalException(StatusCodeEnum.QUESTION_INFO_ERR)

def question_info_list(request):
    """
    查询 QuestionInfo 记录
    """
    try:
        # 1. 提取分页参数
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        # 2. 处理筛选参数
        filters = {}
        for key, value in request.GET.lists():  # 使用lists()获取所有值
            if key in ['page', 'page_size']:
                continue  # 跳过分页参数
            else:
                # 其他参数取第一个值（或根据需求调整）
                filters[key] = value[0] if value else None
        # 3. 查询数据
        filtered_problem = list_problem(**filters)
        paginator = MyPaginator(filtered_problem, page, page_size)
        return ok(paginator.to_response())

    except Exception as e:
        raise GlobalException(StatusCodeEnum.QUESTION_INFO_ERR)

def question_info_get(request):
    """
    查询 QuestionInfo 记录
    """
    question_id = request.GET.get('question_id')
    try:
        code_info = QuestionInfo.objects.get(question_id=question_id)
        return ok(model_to_dict(code_info))
    except QuestionInfo.DoesNotExist:
        raise ValueError(f"QuestionInfo for question_id {question_id} does not exist")


def question_info_update(request):
    """
    更新 QuestionInfo 记录
    """
    if request.method == 'PUT':
        try:
            # 解析 JSON 数据
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)

            filters = {"question_id": data.get("question_id")}
            updates = {
                "question_raw": data.get("question_raw"),
                "checkpoints_count": data.get("checkpoints_count")
            }
            update_question_info(filters=filters, updates=updates)
            return ok()
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

def question_info_delete(request):
    """
    删除 QuestionInfo 记录
    """
    if request.method == 'DELETE':
        try:
            # 解析 JSON 请求体
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)
            question_id = data.get('question_id')
            QuestionInfo.objects.filter(question_id=question_id).delete()
            return ok()
        except Exception as e:
            raise GlobalException(StatusCodeEnum.QUESTION_INFO_ERR)


@csrf_exempt
def question_info_submit(request):
    """
    创建 QuestionInfo 记录
    """
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            question_id = payload.get("question_id")
            code = payload.get("code")
            result_detail = submit_code(question_id, code)
            answer = "评测结果: " + result_detail.get("status") + '\n'
            answer += "通过测试点数: " + str(result_detail.get("pass")) + '/' + str(result_detail.get('all_test_size')) +  '\n'
            return ok(answer)
        except Exception as e:
            raise GlobalException(StatusCodeEnum.QUESTION_INFO_ERR)

