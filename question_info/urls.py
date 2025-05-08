from django.urls import path
from . import views

urlpatterns = [
    path('create', views.question_info_create, name='question_info_create'),
    path('get', views.question_info_get, name='question_info_get'),
    path('list', views.question_info_list, name='question_info_list'),
    path('update', views.question_info_update, name='question_info_update'),
    path('delete', views.question_info_delete, name='question_info_delete'),
    path('submit', views.question_info_submit, name='question_info_submit'),
]