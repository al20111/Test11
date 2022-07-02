from django.contrib import admin
from .models import Board,Opinion,Store,Staff
# Register your models here.
admin.site.register(Store)
admin.site.register(Board)
admin.site.register(Opinion)
admin.site.register(Staff)