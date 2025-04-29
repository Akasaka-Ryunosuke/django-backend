import jwt
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from config import settings
from utils.enums import StatusCodeEnum
from utils.exceptions import GlobalException
from .models import User
from .services import create_user, check_user
from utils.result import ok
from rest_framework.decorators import api_view
from datetime import datetime, timedelta


@csrf_exempt
@api_view(['POST'])
def register(request):
    try:
        data = request.data
        user_id = create_user(data)
        return ok({'user_id': user_id})
    except Exception as e:
        raise e


@csrf_exempt
@api_view(['POST'])
def login(request):
    try:
        data = request.data
        user = check_user(data)

        new_tokens = generate_tokens(user)
        r_dict = model_to_dict(user)

        return ok({**r_dict, **new_tokens})
    except Exception as e:
        raise e


@csrf_exempt
@api_view(['POST'])
def refresh(request):
    try:
        old_refresh_token = request.data.get('refresh_token')
        decoded = jwt.decode(old_refresh_token, settings.SECRET_KEY,
                             algorithms=['HS256'],
                             options={'verify_exp': False})

        user = User.objects.get(user_id=decoded['user_id'])
        new_tokens = generate_tokens(user)

        return ok(new_tokens)
    except Exception:
        raise GlobalException(StatusCodeEnum.TOKEN_ERR)


def generate_tokens(user):
    # 手动构建 Token Payload
    refresh_payload = {
        'user_id': user.user_id,
        'user_name': user.user_name,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow(),
        'jti': 'unique_jti_here',  # 可选：唯一标识
        'token_type': 'refresh'
    }

    access_payload = {
        'user_id': user.user_id,
        'user_name': user.user_name,
        'exp': datetime.utcnow() + timedelta(minutes=30),  # access_token 有效期
        'iat': datetime.utcnow(),
        'token_type': 'access'
    }

    # 使用 Django 的 SECRET_KEY 签名
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
