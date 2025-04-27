from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .services import create_user, check_user
from utils.result import ok
from rest_framework.decorators import api_view


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
        return ok(model_to_dict(user))
    except Exception as e:
        raise e
