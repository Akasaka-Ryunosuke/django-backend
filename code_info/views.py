from django.views.decorators.csrf import csrf_exempt
from .services import create_code_info, get_code_info, update_code_info, delete_code_info, list_code_info
from django.forms.models import model_to_dict
from utils.result import ok
from utils.exceptions import GlobalException, StatusCodeEnum
from utils.paginator import MyPaginator
from rest_framework.decorators import api_view


@csrf_exempt
@api_view(['POST'])
def code_info_create(request):
    """
    创建 CodeInfo 记录
    """
    try:
        data = request.data
        code_info = create_code_info(data)
        return ok(model_to_dict(code_info))
    except Exception:
        raise GlobalException(StatusCodeEnum.CODE_INFO_ERR)


@csrf_exempt
@api_view(['DELETE'])
def code_info_delete(request):
    """
    通过 code_id 删除 CodeInfo 记录
    """
    try:
        code_id = request.GET.get('code_id')
        if not code_id:
            raise GlobalException(StatusCodeEnum.PARAM_ERR)
        delete_code_info(code_id=int(code_id))
        return ok()
    except Exception:
        raise GlobalException(StatusCodeEnum.CODE_INFO_ERR)


@csrf_exempt
@api_view(['PUT'])
def code_info_update(request):
    """
    更新 CodeInfo 记录
    """
    try:
        data = request.data
        code_id = request.GET.get('code_id')
        if not code_id:
            raise GlobalException(StatusCodeEnum.PARAM_ERR)
        updates = {
            "user_id": data.get("user_id"),
            "question_id": data.get("question_id"),
            "code_raw": data.get("code_raw"),
            "code_type": data.get("code_type"),
            "score": data.get("score"),
            "run_time": data.get("run_time"),
            "upload_time": data.get("upload_time")
        }
        update_code_info(code_id=int(code_id), updates=updates)
        code_info = get_code_info(code_id)
        return ok(model_to_dict(code_info))
    except Exception:
        raise GlobalException(StatusCodeEnum.CODE_INFO_ERR)


@csrf_exempt
@api_view(['GET'])
def code_info_get(request):
    """
    查询 CodeInfo 记录
    """
    try:
        code_id = request.GET.get('code_id')
        if not code_id:
            raise GlobalException(StatusCodeEnum.PARAM_ERR)
        code_info = get_code_info(code_id=int(code_id))
        return ok(model_to_dict(code_info))
    except Exception:
        raise GlobalException(StatusCodeEnum.CODE_INFO_ERR)


@csrf_exempt
@api_view(['GET'])
def code_info_list(request):
    """
    查询 CodeInfo 记录并支持分页
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

            if key == 'code_type':
                # code_type 直接使用列表形式
                filters[key] = value
            else:
                # 其他参数取第一个值（或根据需求调整）
                filters[key] = value[0] if value else None

        # 3. 查询数据
        filtered_code_info = list_code_info(**filters)
        paginator = MyPaginator(filtered_code_info, page, page_size)
        return ok(paginator.to_response())

    except Exception as e:
        raise GlobalException(StatusCodeEnum.CODE_INFO_ERR)
