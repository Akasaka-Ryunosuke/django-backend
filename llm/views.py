import json

from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils.result import ok
from .models import LlmRecord, Detail
from django.utils import timezone
from rest_framework.decorators import api_view
from code_info.models import CodeInfo
from question_info.models import QuestionInfo
from .chat import get_response
from utils.exceptions import GlobalException,StatusCodeEnum


# 1. 创建一个会话
@csrf_exempt
@api_view(['POST'])
def create_session(request):
    data = request.data
    user_id = data.get('user_id')
    question_id = data.get('question_id')
    mode = data.get('mode')

    if user_id is None or question_id is None or mode is None:
        return JsonResponse({'error': 'user_id and question_id are required'}, status=400)

    session = LlmRecord.objects.create(
        user_id=user_id,
        question_id=question_id,
        mode=mode,
        upload_time=timezone.now()
    )
    return ok({'llm_record_id': session.llm_record_id})


# 2. 根据 user_id 和 question_id 搜索所有会话，并在 json 中以 list 形式返回
@csrf_exempt
@api_view(['GET'])
def search_sessions(request):
    user_id = request.GET.get('user_id')
    question_id = request.GET.get('question_id')
    mode = request.GET.get('mode')

    if user_id is None or question_id is None or mode is None:
        return JsonResponse({'error': 'user_id, question_id and mode are required'}, status=400)

    sessions = LlmRecord.objects.filter(user_id=user_id, question_id=question_id, mode=mode).order_by('-upload_time')

    return ok({'sessions': list(sessions.values())})


# 3. 根据会话 id 接收并添加会话内容，调用外部模型函数
# 并将模型返回值存入相同会话，并返回模型返回值
@csrf_exempt
def add_session_detail(request):
    data = json.loads(request.body.decode('utf-8'))
    llm_record_id = data.get('llm_record_id')
    raw = data.get('raw')

    if raw is None:
        return JsonResponse({'error': 'raw content is required'}, status=400)

    messages = []
    try:
        session = LlmRecord.objects.get(llm_record_id=llm_record_id)
        details = Detail.objects.filter(llm_record_id=llm_record_id).order_by('upload_time')
        for detail in details:
            if detail.io_type == 1:
                messages.append({"role": "user", "content": detail.raw})
            else:
                messages.append({"role": "assistant", "content": detail.raw})
    except LlmRecord.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
    messages.append({"role": "user", "content": raw})

    # 保存用户输入
    Detail.objects.create(
        llm_record_id=llm_record_id,
        io_type=1,
        raw=raw,
        upload_time=timezone.now()
    )

    question_info = QuestionInfo.objects.get(question_id=session.question_id)
    question_raw = question_info.question_raw
    try:
        code_info = CodeInfo.objects.filter(user_id=session.user_id, question_id=session.question_id).order_by("upload_time").last()
        code_raw = code_info.code_raw
    except CodeInfo.DoesNotExist:
        raise GlobalException(StatusCodeEnum.CODE_RAW_BLANK_ERR)

    def event_stream():
        collected_chunks = []
        # 调用流式生成器
        for chunk in get_response(session.mode, messages, question_raw, code_raw):
            collected_chunks.append(chunk)
            # 使用SSE格式发送每个数据块
            yield f"data: {json.dumps({'llm_response': chunk})}\n\n"

        # 流式结束后保存完整响应到数据库
        full_response = ''.join(collected_chunks)
        Detail.objects.create(
            llm_record_id=llm_record_id,
            io_type=0,
            raw=full_response,
            upload_time=timezone.now()
        )

    return StreamingHttpResponse(
        event_stream(),
        content_type='text/event-stream'  # 使用SSE内容类型
    )


# 4. 根据会话 id 查询会话内容
@csrf_exempt
@api_view(['GET'])
def get_session_detail(request):
    llm_record_id = request.GET.get('llm_record_id')
    if llm_record_id is None:
        return JsonResponse({'error': 'llm_record_id is required'}, status=400)
    session = LlmRecord.objects.get(llm_record_id=llm_record_id)
    details = Detail.objects.filter(llm_record_id=llm_record_id).order_by('upload_time')
    return ok({
        'llm_record_id': session.llm_record_id,
        'user_id': session.user_id,
        'question_id': session.question_id,
        'upload_time': session.upload_time.strftime('%Y-%m-%d %H:%M:%S') if session.upload_time else None,
        'details': list(details.values())
    })
