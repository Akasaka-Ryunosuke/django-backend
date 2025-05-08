from django.urls import path
from .views import create_session, search_sessions, add_session_detail, get_session_detail

urlpatterns = [
    path('create_session', create_session, name='create_session'),
    path('list_session', search_sessions, name='search_sessions'),
    path('add_session_detail', add_session_detail, name='add_session_detail'),
    path('get_session_detail', get_session_detail, name='get_session_detail'),
]
