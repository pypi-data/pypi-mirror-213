from django.urls import path

from .views import admin_resumable

urlpatterns = [
    path('admin_resumable/', admin_resumable, name='admin_resumable'),
]
