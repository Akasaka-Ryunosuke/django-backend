import logging
from django.http.response import JsonResponse
from django.middleware.common import MiddlewareMixin
from .enums import StatusCodeEnum
from utils.exceptions import GlobalException

logger = logging.getLogger('django')


class ExceptionMiddleware(MiddlewareMixin):
    """统一异常处理中间件"""

    def process_exception(self, request, exception):
        """
        统一异常处理
        :param request: 请求对象
        :param exception: 异常对象
        :return:
        """
        if isinstance(exception, GlobalException):
            return exception.to_response()
        else:
            logger.error(exception)
            result = {
                "code": StatusCodeEnum.SERVER_ERR.code,
                "message": StatusCodeEnum.SERVER_ERR.errmsg,
            }
            return JsonResponse(
                result,
                status=StatusCodeEnum.SERVER_ERR.status,
                json_dumps_params={'ensure_ascii': False}
            )
