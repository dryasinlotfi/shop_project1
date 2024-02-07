from django.contrib import admin
from .models import User, OTPRequest
# Register your models here.


@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff']


@admin.register(OTPRequest)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['channel', 'receiver']