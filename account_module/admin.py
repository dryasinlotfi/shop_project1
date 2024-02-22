from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from account_module.forms import UserChangeForm
from account_module.models import User, OtpCode

# Register your models here.

    
admin.site.unregister(Group)


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'code', 'created']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    list_display = ['username', 'email', 'is_superuser']
    list_filter = ['is_superuser', ]

    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'username', 'password')}),
        ("Permissions", {'fields': ('is_active', 'is_superuser', 'last_login')}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'username', 'password', "confirm_password")}),

    )

    search_fields = ('email', 'phone_number', 'username')
    ordering = ('username',)

    filter_horizontal = ()


