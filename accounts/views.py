from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .models import User
from utils.result import ok
from utils.exceptions import GlobalException, StatusCodeEnum
import json


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # 验证密码是否为空
        if data['user_password'] == "":
            raise GlobalException(StatusCodeEnum.PASSWORD_BLANK_ERR)

        # 验证用户名是否已存在
        if User.objects.filter(user_name=data['user_name']).exists():
            raise GlobalException(StatusCodeEnum.USER_EXIST_ERR)

        # 默认普通用户
        user = User(
            user_name=data['user_name'],
            user_type='user'
        )
        user.set_password(data['user_password'])
        user.save()

        return ok({'user_id': user.user_id})
    else:
        raise GlobalException(StatusCodeEnum.METHOD_ERR)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.get(user_name=data['user_name'])
            if user.check_password(data['user_password']):
                return ok({
                    'user_id': user.user_id,
                    'user_type': user.user_type
                })
            else:
                raise GlobalException(StatusCodeEnum.PASSWORD_WRONG_ERR)

        except ObjectDoesNotExist:
            raise GlobalException(StatusCodeEnum.USER_NOT_EXIST_ERR)
    else:
        raise GlobalException(StatusCodeEnum.METHOD_ERR)
