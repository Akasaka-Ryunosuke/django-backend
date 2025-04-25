from .enums import StatusCodeEnum
from django.http import JsonResponse


def ok(data=None) -> JsonResponse:
    """成功响应快捷函数"""
    payload = {
        "success": True,
        "code": StatusCodeEnum.OK.code,
        "message": StatusCodeEnum.OK.errmsg,
        "data": data or {}
    }
    return JsonResponse(
        payload,
        status=StatusCodeEnum.OK.status,
        json_dumps_params={'ensure_ascii': False}
    )
