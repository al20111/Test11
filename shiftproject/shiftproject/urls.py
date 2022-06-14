from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('account.urls')),
    path('shift/',include('shift.urls')),
    path('message/',include('message.urls')),
]
