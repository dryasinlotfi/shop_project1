import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField as PhoneNumber
# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/profile', verbose_name='تصویر پروفایل', null=True, blank=True )
    email_active_code = models.CharField(max_length=100, verbose_name='کد فعالسازی ایمیل ', null=True)
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره کاربر')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    phone_number = PhoneNumber(blank=True, max_length=22, null=True, verbose_name='شماره همراه', unique=True)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return self.get_full_name()
        return self.email


class OTPRequest(models.Model):
    class OTPChannel(models.TextChoices):
        PHONE = 'phone'
        EMAIL = 'E-MAIL'
    request_id = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    channel = models.CharField(max_length=10, choices=OTPChannel.choices, default=OTPChannel.PHONE)
    receiver = models.CharField(max_length=50)
    password = models.CharField(max_length=4)
    created = models.DateTimeField(auto_now=True, editable=False)

