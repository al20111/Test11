from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
admin.site.register(User)

class AdminUserAdmin(UserAdmin):
    fieldsets=(
        (None,{"fields":("username","password")}),
        ("Personal info",{"fields":("email")}),
        ("Permissions",{"fields":("is_active","is_member","is_staff","is_superuser","groups","user_permissions")}),
        ("Important dates",{"fields":("last_login","date_joined")}),
    )

    list_display=("username","is_member","last_login")
    search_fields=("username","email")
    filter_horizontal=("groups","user_permissions")

