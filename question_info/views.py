from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from utils.result import ok
from .services import create_question_info, get_question_info, update_question_info, delete_question_info

@csrf_exempt
def question_info_create(request):
    """
    创建 QuestionInfo 记录
    """
    if request.method == 'POST':
        try:
            data = request.POST  # 获取 POST 数据
            question_info = create_question_info(
                question_id=data.get('question_id'),
                question_raw=data.get('question_raw'),
                checkpoints_count=data.get('checkpoints_count')
            )
            return JsonResponse({"status": "success", "data": str(question_info)})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

def question_info_list(request):
    """
    查询 QuestionInfo 记录
    """
    if request.method == 'GET':
        try:
            filters = {key: str(value) for key, value in request.GET.items()}  # 确保值是字符串
            question_records = get_question_info(**filters)
            data = [{"question_id": record.question_id, "question_raw": record.question_raw,
                     "checkpoints_count": record.checkpoints_count} for record in question_records]
            return ok(data[0])
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

def question_info_update(request):
    """
    更新 QuestionInfo 记录
    """
    if request.method == 'PUT':
        try:
            data = request.POST  # 获取 PUT 数据
            filters = {"question_id": data.get("question_id")}
            updates = {
                "question_raw": data.get("question_raw"),
                "checkpoints_count": data.get("checkpoints_count")
            }
            update_question_info(filters=filters, updates=updates)
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

def question_info_delete(request):
    """
    删除 QuestionInfo 记录
    """
    if request.method == 'DELETE':
        try:
            filters = {key: value for key, value in request.GET.items()}
            delete_question_info(**filters)
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)