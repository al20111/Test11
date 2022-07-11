from django.contrib.auth import validators
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

class User(AbstractBaseUser,PermissionsMixin):
    username_validators=UnicodeUsernameValidator()
    username=models.CharField(
        "name",
        max_length=20,
        unique=True,
        help_text="※20文字以下で入力してください",
        validators=[username_validators],
        error_messages={
            "unique":"このユーザー名は既に使用されています．",
        },
    )

    email=models.EmailField("Eメールアドレス",blank=True,null=True)

    is_staff=models.BooleanField(
        "ユーザーステータス",
        help_text="ユーザーがこの管理サイトにログインできるかどうかを指定します.アカウントを削除する代わりに，これを非アクティブに",
        default=False,
    )
    is_member=models.BooleanField(
        "会員ステータス",
        help_text="このユーザが契約しているかを区別します.",
        default=False,
    )
    is_active=models.BooleanField(
        "アクティブユーザー",
        help_text="このユーザーをアクティブとして扱うかどうかを指定します．アカウントを削除する代わりに",
        default=True,
    )
    date_joined=models.DateTimeField("登録日",default=timezone.now)
    objects=UserManager()

    EMAIL_FIELD='email'
    USERNAME_FIELD='username'
    class Meta:
        verbose_name="user"
        verbose_name_plural="users"
 
    def clean(self):
        super().clean()
        self.email=self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
