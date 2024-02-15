from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField as PhoneNumber

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # Validators should be a lis


# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/profile', verbose_name='تصویر پروفایل', null=True, blank=True )
    email_active_code = models.CharField(max_length=100, verbose_name='کد فعالسازی ایمیل ', null=True)
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره کاربر')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    phone_number = PhoneNumber(blank=True, max_length=17,validators=[phone_regex], null=True, verbose_name='شماره همراه', unique=True)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return self.get_full_name()
        return self.email



