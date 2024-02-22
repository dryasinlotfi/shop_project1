import random

from account_module.models import OtpCode
from utils import send_top_code
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from account_module.forms import RegisterForm, LoginForm, ForgetPasswordForm


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)

    def post(self, request, send_top_cod):
        register_form = RegisterForm
        if register_form.is_valid():
            random_code = random.randint(10000, 99999)
            send_top_cod(register_form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=register_form.cleaned_data['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': register_form.cleaned_data['phone_number'],
                'email': register_form.cleaned_data['email'],
                'username': register_form.cleaned_data['username'],
                'password': register_form.cleaned_data['password']
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')
        return redirect('home:home')


class UserRegisterVerifyCodeView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class LoginView(View):
    def get(self, request):
        login_form = LoginForm
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)


class ForgetPasswordView(View):
    def get(self, request):
        forget_form = ForgetPasswordForm
        context = {
            'forget_form': forget_form
        }
        return render(request, 'account_module/forget_password.html', context)