from django.contrib import admin
from django.urls import path
from mentor.views import ask_ai  # <--- This connects to your brain!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ask_ai/', ask_ai),
]
