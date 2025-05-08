from django.urls import path
from . import views

urlpatterns = [
    path('create', views.code_info_create, name='code_info_create'),
    path('delete', views.code_info_delete, name='code_info_delete'),
    path('update', views.code_info_update, name='code_info_update'),
    path('get', views.code_info_get, name='code_info_get'),
    path('list', views.code_info_list, name='code_info_list'),
]