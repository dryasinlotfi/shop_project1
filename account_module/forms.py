
from django.core import validators
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import phonenumbers
from phonenumbers import PhoneNumber


class RegisterForm(forms.Form):
    phone_number = forms.IntegerField(
        label='شماره تلفن',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'email'})
    )
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'username'}),
        validators=[
            validators.MaxLengthValidator(15)
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

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password


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