# Generated by Django 3.2.19 on 2023-06-24 17:45

import accounts.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=' ', help_text='You can use a-z, 0-9 and underscore. Minimum length in 5 character.', max_length=15, unique=True, validators=[accounts.validators.UsernameValidator(), django.core.validators.MinLengthValidator(5)], verbose_name='Username'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(null=True, validators=[accounts.validators.AgeValidator()], verbose_name='Date of birth'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_image/', verbose_name='Profile image'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
