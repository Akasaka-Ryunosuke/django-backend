from django.http import JsonResponse
from .enums import StatusCodeEnum


class GlobalException(Exception):
    """基础API异常"""

    def __init__(self, enum: StatusCodeEnum):
        self.code = enum.code
        self.status = enum.status
        self.message = enum.errmsg
        super().__init__(self.message)

    def to_response(self) -> JsonResponse:
        """将异常转换为响应对象"""
        payload = {
            "code": self.code,
            "message": self.message
        }
        return JsonResponse(
            payload,
            status=self.status,
        )
