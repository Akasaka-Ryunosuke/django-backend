from django.http import JsonResponse
from .services import create_code_info, get_code_info, update_code_info, delete_code_info

def code_info_create(request):
    """
    创建 CodeInfo 记录
    """
    if request.method == 'POST':
        try:
            data = request.POST  # 获取 POST 数据
            code_info = create_code_info(
                user_id=data.get('user_id'),
                question_id=data.get('question_id'),
                code_raw=data.get('code_raw'),
                code_type=data.get('code_type'),
                score=data.get('score'),
                run_time=data.get('run_time'),
                upload_time=data.get('upload_time')
            )
            return JsonResponse({"status": "success", "data": str(code_info)})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

def code_info_list(request):
    """
    查询 CodeInfo 记录
    """
    if request.method == 'GET':
        try:
            filters = {key: value for key, value in request.GET.items()}
            code_records = get_code_info(**filters)
            data = [{"code_id": record.code_id, "user_id": record.user_id, "question_id": record.question_id,
                     "code_raw": record.code_raw, "score": float(record.score)} for record in code_records]
            return JsonResponse({"status": "success", "data": data})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

def code_info_update(request):
    """
    更新 CodeInfo 记录
    """
    if request.method == 'PUT':
        try:
            data = request.POST  # 获取 PUT 数据
            filters = {"code_id": data.get("code_id")}
            updates = {
                "user_id": data.get("user_id"),
                "question_id": data.get("question_id"),
                "code_raw": data.get("code_raw"),
                "code_type": data.get("code_type"),
                "score": data.get("score"),
                "run_time": data.get("run_time"),
                "upload_time": data.get("upload_time")
            }
            update_code_info(filters=filters, updates=updates)
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

def code_info_delete(request):
    """
    删除 CodeInfo 记录
    """
    if request.method == 'DELETE':
        try:
            filters = {key: value for key, value in request.GET.items()}
            delete_code_info(**filters)
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)