# Generated by Django 4.2.9 on 2024-02-21 23:01

import django.core.validators
from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0008_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=17, null=True, region=None, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\d{9,15}$')], verbose_name='شماره همراه'),
        ),
    ]
