from django.contrib import admin

from account_module.models import User


# Register your models here.


@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff']


