import random

from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest

from account_module.models import OtpCode, User
from utils import send_otp_code
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from account_module.forms import RegisterForm, LoginForm, ForgetPasswordForm, UserRegistrationForm, VerifyCodeForm


class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account_module/register.html'

    def get(self, request):
        register_form = self.form_class
        context = {
            'register_form': register_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        register_form = self.form_class(request.POST)
        if register_form.is_valid():
            phone_number = register_form.cleaned_data['phone_number']
            email = register_form.cleaned_data['email']
            if User.objects.filter(phone_number=phone_number).exists() or User.objects.filter(email=email).exists():
                messages.error(request, 'شماره تلفن یا ایمیل استفاده شده است')
                return render(request, self.template_name, {'form': register_form})
            else:
                random_code = random.randint(1000, 9999)
                send_otp_code(register_form.cleaned_data['phone_number'], random_code)
                OtpCode.objects.create(phone_number=register_form.cleaned_data['phone_number'], code=random_code)
                request.session['user_registration_info'] = {
                    'phone_number': register_form.cleaned_data['phone_number'],
                    'email': register_form.cleaned_data['email'],
                    'username': register_form.cleaned_data['username'],
                    'password': register_form.cleaned_data['password']
                }
                messages.success(request, 'we sent you a code', 'success')
                return redirect('verify_form')

        return render(request, self.template_name, {'form': register_form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'account_module/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.filter(phone_number=user_session['phone_number']).last()
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if int(cd['code']) == int(code_instance.code):
                User.objects.create_user(user_session['phone_number'], user_session['email'],
                                         user_session['username'], user_session['password'])
                messages.success(request, 'you registered.', 'success')
                otp_all = OtpCode.objects.filter(phone_number=user_session['phone_number']).all()
                otp_all.delete()
                return redirect('home_page')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('verify_form')
        return redirect('verify_form')


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_phone_number = login_form.cleaned_data.get('phone_number')
            user_password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(phone_number__iexact=user_phone_number).first()
            if user is not None:
                is_password_correct = user.check_password(user_password)
                if is_password_correct:
                    login(request, user)
                    return redirect(reverse('home_page'))
                else:
                    login_form.add_error('phone_number', 'شماره وارد شده نامعتبر است')
        else:
            login_form.add_error('phone_number', 'کاربری با مشخصات وارد شده یافت نشد')

        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context)


@method_decorator(login_required, name='dispatch')
class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        logout(request)
        messages.success(request, 'شما با موفقیت از حساب خود خارج شدید ', 'success')
        return redirect('home_page')


class ForgetPasswordView(View):
    def get(self, request):
        forget_form = ForgetPasswordForm
        context = {
            'forget_form': forget_form
        }
        return render(request, 'account_module/forget_password.html', context)