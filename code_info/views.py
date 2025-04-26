from django.core.paginator import Paginator
from django.http import JsonResponse
from .services import create_code_info, get_code_info, update_code_info, delete_code_info
from utils.result import ok

def code_info_create(request):
    """
    创建 CodeInfo 记录
    """
    if request.method == 'POST':
        try:
            data = request.POST  # 获取 POST 数据
            code_info = create_code_info(
                user_id=data.get('user_id'),
                question_id=data.get('question_id'),
                code_raw=data.get('code_raw'),
                code_type=data.get('code_type'),
                score=data.get('score'),
                run_time=data.get('run_time'),
                upload_time=data.get('upload_time')
            )
            return JsonResponse({"status": "success", "data": str(code_info)})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

def code_info_list(request):
    """
    查询 CodeInfo 记录并支持分页
    """
    if request.method == 'GET':
        try:
            # 1. 获取过滤参数
            filters = {key: value for key, value in request.GET.items() if key not in ['page', 'page_size']}

            # 2. 获取分页参数，并提供默认值和类型转换
            try:
                page_number = int(request.GET.get('page', 1)) # 默认第1页
                page_size = int(request.GET.get('page_size', 10)) # 默认每页10条
                if page_number < 1:
                    page_number = 1
                if page_size < 1:
                     page_size = 10 # 避免负数或0导致问题
            except ValueError:
                # 参数不是有效的整数，返回错误
                return JsonResponse({"success": False, "message": "Invalid pagination parameters."}, status=400)


            # 3. 应用过滤条件，获取符合条件的所有记录（在分页之前）
            # get_code_info 需要返回一个 QuerySet 或者一个支持切片和 count() 的对象
            all_filtered_records = get_code_info(**filters)

            # 4. 获取总记录数 (在应用切片之前)
            total_count = all_filtered_records.count() # 假设 get_code_info 返回 QuerySet，支持 count()

            # 5. 使用 Django 的 Paginator 进行分页处理
            paginator = Paginator(all_filtered_records, page_size)

            try:
                # 获取当前页的数据
                page_obj = paginator.page(page_number)
                code_records = page_obj.object_list # 当前页的记录列表
            except Exception: # 可以捕获 InvalidPage 异常等
                 # 如果页码超出范围，返回空数据或者第一页数据，这里返回空并提示错误
                 code_records = []
                 # Optional: Return an error or just empty data
                 # return JsonResponse({"success": False, "message": "Page number out of range."}, status=400)

            # 6. 格式化当前页的数据 (列表形式)
            current_page_records_list = [
                {"code_id": record.code_id, "user_id": record.user_id, "question_id": record.question_id,
                 "code_type": record.code_type, "score": float(record.score), "date": record.upload_time} for record in
                code_records]

            # 7. 构建一个字典，将所有需要返回的数据（包括记录列表和分页信息）打包
            #    这个字典将作为参数传给原始的 ok 函数的 data 参数
            response_payload_data = {
                "list": current_page_records_list,  # 将当前页的记录列表放在 'list' 字段里
                "total": total_count,  # 总记录数
                "page": page_number,  # 当前页码
                "page_size": page_size  # 每页数量
            }

            # 8. 调用原始的 ok 函数，将构建好的字典作为 data 参数传入
            return ok(data=response_payload_data)

        except Exception as e:
            # 其他内部错误处理
            print(f"Error in code_info_list: {e}") # 打印到后端控制台方便调试
            return JsonResponse({"success": False, "message": str(e)}, status=500) # 返回 500 错误

    else:
        # 方法不被允许
        return JsonResponse({"success": False, "message": "Method Not Allowed"}, status=405)


def code_info_update(request):
    """
    更新 CodeInfo 记录
    """
    if request.method == 'PUT':
        try:
            data = request.POST  # 获取 PUT 数据
            filters = {"code_id": data.get("code_id")}
            updates = {
                "user_id": data.get("user_id"),
                "question_id": data.get("question_id"),
                "code_raw": data.get("code_raw"),
                "code_type": data.get("code_type"),
                "score": data.get("score"),
                "run_time": data.get("run_time"),
                "upload_time": data.get("upload_time")
            }
            update_code_info(filters=filters, updates=updates)
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

def code_info_delete(request):
    """
    删除 CodeInfo 记录
    """
    if request.method == 'DELETE':
        try:
            filters = {key: value for key, value in request.GET.items()}
            delete_code_info(**filters)
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)