from django.contrib import admin
from django.urls import path
from mentor.views import ask_ai
from django.views.generic import TemplateView

urlpatterns = [
    # 1. Django Admin Panel
    path('admin/', admin.site.urls),

    # 2. AI Backend Logic (where the voice transcript goes)
    path('ask_ai/', ask_ai),

    # 3. The Frontend (serves your index.html)
    path('', TemplateView.as_view(template_name="index.html"), name='home'),
]

# Static files are now served by WhiteNoise middleware in production.
# No need for manual static URL patterns.