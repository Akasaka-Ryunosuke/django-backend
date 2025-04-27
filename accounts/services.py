from typing import Dict
from django.db import transaction
from utils.enums import StatusCodeEnum
from utils.exceptions import GlobalException
from .models import User


def create_user(data: Dict):
    # 验证密码是否为空
    if data['user_password'] == "":
        raise GlobalException(StatusCodeEnum.PASSWORD_BLANK_ERR)

    # 验证用户名是否已存在
    if User.objects.filter(user_name=data['user_name']).exists():
        raise GlobalException(StatusCodeEnum.USER_EXIST_ERR)

    try:
        with transaction.atomic():
            user = User(
                user_name=data['user_name'],
                user_type='user'
            )
            user.set_password(data['user_password'])
            user.save()
            return user.user_id
    except Exception:
        raise GlobalException(StatusCodeEnum.ACCOUNT_ERR)


def check_user(data: Dict) -> User:
    try:
        user = User.objects.get(user_name=data['user_name'])
        if user.check_password(data['user_password']):
            return user
        else:
            raise GlobalException(StatusCodeEnum.PASSWORD_WRONG_ERR)
    except User.DoesNotExist:
        raise GlobalException(StatusCodeEnum.USER_NOT_EXIST_ERR)
