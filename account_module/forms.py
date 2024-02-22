
from django.core import validators
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import phonenumbers
from phonenumbers import PhoneNumber

from account_module.models import User, OtpCode


class RegisterForm(forms.ModelForm):
    phone_number = forms.CharField(
        label='شماره تلفن',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'username'}),
        validators=[
            validators.MaxLengthValidator(15)
        ]
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control','type': 'password'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control','type': 'password'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'username')

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd ['password'] and cd['confirm_password'] and cd['password'] != cd['confirm_password']:
            raise ValidationError('password dont match')
        return cd['confirm_password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email'})
    )
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'username'}),
    )
    phone_number = forms.CharField(
        max_length=11,
        label='شماره تلفن',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'passwrd'}),
        label='کلمه عبور',
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists')
        return email

    def clean_phone(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('This phone number already exists')
        OtpCode.objects.filter(phone_number=phone_number).delete()
        return phone_number

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you cant change password <a href=\".../password/\"> this form </a>. ')

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'username', 'password', 'last_login')


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()

    # def clean_confirm_password(self):
    #     password = self.cleaned_data.get('password')
    #     confirm_password = self.cleaned_data.get('confirm_password')
    #
    #     if password == confirm_password:
    #         return confirm_password


class LoginForm(forms.Form):
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'username'}),
        validators=[
            validators.MaxLengthValidator(15)
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )


class ForgetPasswordForm(forms.Form):
    phone_number = forms.IntegerField(
        label='شماره تلفن',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'email'})
    )
    code = forms.IntegerField(
        label='کد یکبار مصرف',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}),
        validators=[
            validators.MaxLengthValidator(5),
        ]

    )