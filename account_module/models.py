from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField as PhoneNumber

from account_module.managers import UserManager

# vlaidation
phone_regex = RegexValidator(regex=r'09\d{9}',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")  # Validators should be a lis
username_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9]([._-](?![._-])|[a-zA-Z0-9]){3,18}[a-zA-Z0-9]$',
    message='Username must start with an alphanumeric character, contain between 3 and 18 of the following: alphanumeric characters, dots, hyphens, or underscores, and end with an alphanumeric character',
    code='invalid_username',
)
password_validator = RegexValidator(
    regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$',
    message='Password must contain at least one lowercase letter, one uppercase letter, one digit, and be at least 8 characters long',
    code='invalid_password',
)

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to='images/profile', verbose_name='تصویر پروفایل', null=True, blank=True )
    username = models.CharField(max_length=20, unique=True, validators=[username_validator], verbose_name='نام کاربری')
    email_active_code = models.CharField(max_length=100, verbose_name='کد فعالسازی ایمیل ', null=True)
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره کاربر')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    phone_number = models.CharField(blank=True, max_length=11, null=True, verbose_name='شماره همراه', unique=True)
    is_verified = models.BooleanField(default=False, verbose_name="کاربر فعال/ غیر فعال")
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'username']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        if self.first_name != '' and self.last_name != '':
            return self.get_full_name()
        return self.email


class OtpCode(models.Model):
    phone_number = models.CharField()
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} -  {self.code} - {self.created}'

