from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .services import create_user, check_user
from utils.result import ok
from utils.exceptions import GlobalException, StatusCodeEnum



@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = request.POST.dict()
            user_id = create_user(data)
            return ok({'user_id': user_id})
        except Exception:
            raise GlobalException(StatusCodeEnum.ACCOUNT_ERR)
    else:
        raise GlobalException(StatusCodeEnum.METHOD_ERR)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = request.POST.dict()
            user = check_user(data)
            return ok(model_to_dict(user))
        except Exception as e:
            raise e
    else:
        raise GlobalException(StatusCodeEnum.METHOD_ERR)
