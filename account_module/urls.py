
from django.urls import path
from .views import RegisterView, LoginView, ForgetPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_form'),
    path('login/', LoginView.as_view(), name='login_form'),
    path('forget/', ForgetPasswordView.as_view(), name='forget_form'),
]