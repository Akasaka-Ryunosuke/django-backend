from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # 验证密码是否为空
            if data['user_password'] == "":
                return JsonResponse({'status': 'error', 'message': '密码不能为空'})

            # 验证用户名是否已存在
            if User.objects.filter(user_name=data['user_name']).exists():
                return JsonResponse({'status': 'error', 'message': '用户名已存在'})

            # 默认普通用户
            user = User(
                user_name=data['user_name'],
                user_type='user'
            )
            user.set_password(data['user_password'])
            user.save()

            return JsonResponse({'status': 'success', 'user_id': user.user_id})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.get(user_name=data['user_name'])
            if user.check_password(data['user_password']):
                return JsonResponse({
                    'status': 'success',
                    'user_id': user.user_id,
                    'user_type': user.user_type
                })
            else:
                return JsonResponse({'status': 'error', 'message': '密码错误'})

        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': '用户不存在'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
