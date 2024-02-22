
from django.urls import path
from .views import RegisterView, LoginView, ForgetPasswordView, UserRegisterVerifyCodeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_form'),
    path('verify/', UserRegisterVerifyCodeView.as_view(), name='verify_form'),
    path('login/', LoginView.as_view(), name='login_form'),
    path('forget/', ForgetPasswordView.as_view(), name='forget_form'),
]