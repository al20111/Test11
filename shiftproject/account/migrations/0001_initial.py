# Generated by Django 3.2 on 2022-06-27 09:22

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'このユーザー名は既に使用されています．'}, help_text='※20文字以下で入力してください', max_length=20, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Eメールアドレス')),
                ('is_staff', models.BooleanField(default=False, help_text='ユーザーがこの管理サイトにログインできるかどうかを指定します.アカウントを削除する代わりに，これを非アクティブに', verbose_name='ユーザーステータス')),
                ('is_member', models.BooleanField(default=False, help_text='このユーザが契約しているかを区別します.', verbose_name='会員ステータス')),
                ('is_active', models.BooleanField(default=True, help_text='このユーザーをアクティブとして扱うかどうかを指定します．アカウントを削除する代わりに', verbose_name='アクティブユーザー')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]