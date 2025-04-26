from django.urls import path
from . import views

urlpatterns = [
    path('create', views.code_info_create, name='code_info_create'),
    path('list', views.code_info_list, name='code_info_list'),
    path('update', views.code_info_update, name='code_info_update'),
    path('delete', views.code_info_delete, name='code_info_delete'),
]