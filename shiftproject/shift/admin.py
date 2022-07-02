from django.contrib import admin
from .models import Message,Board,Opinion,Store,Staff
# Register your models here.
admin.site.register(Message)
admin.site.register(Store)
admin.site.register(Board)
admin.site.register(Opinion)
admin.site.register(Staff)