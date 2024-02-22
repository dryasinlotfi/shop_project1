import random

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
        return redirect('home_page')


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = VerifyCodeForm
        return render(request, 'account_module/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                if cd['code'] == code_instance.code:
                    User.objects.create_user(user_session['phone_number'], user_session['email'],
                                             user_session['username'], user_session['password'])
                    code_instance.delete()
                    messages.success(request, 'you registered', 'success')
                    return redirect('home_page')
                else:
                    messages.error(request, 'this code is wrong', 'danger')
                    return redirect('verify_form')
            return redirect('home_page')



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