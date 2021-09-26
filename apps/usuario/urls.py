# from allauth.account.views import confirm_email
from django.urls import path, include
from .views import UsuarioListViewSet, UsuarioDetailUpdateViewSet, CustomRegisterView
from .api import UserAPIView

urlpatterns = [
    path('usuario/', UserAPIView.as_view()),
]
