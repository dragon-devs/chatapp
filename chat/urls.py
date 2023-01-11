from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.personal_chat_view, name='personal-chat'),
    path('', views.chat_view, name='chat'),
]
