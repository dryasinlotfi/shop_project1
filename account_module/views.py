from django.shortcuts import render
from django.views import View
from account_module.forms import RegisterForm, LoginForm, ForgetPasswordForm


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)

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