from django.core.paginator import Paginator, EmptyPage
from django.forms.models import model_to_dict


class MyPaginator:
    """
    分页工具
    """

    def __init__(self, queryset, page, page_size):
        self.queryset = queryset
        try:
            self.page = max(1, int(page))
        except (TypeError, ValueError):
            self.page = 1

        try:
            self.page_size = max(1, int(page_size))
        except (TypeError, ValueError):
            self.page_size = 10

    def to_response(self):
        """
        生成响应
        """
        paginator = Paginator(self.queryset, self.page_size)
        try:
            page = paginator.page(self.page)
            data = [model_to_dict(obj) for obj in page]
        except EmptyPage:
            data = []

        return {
            "list": data,
            "total": paginator.count,
            "page": self.page,
            "page_size": self.page_size
        }
