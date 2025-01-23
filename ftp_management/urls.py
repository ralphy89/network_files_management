from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('files', views.files_management, name='files_management'),
    path('upload-f', views.upload_files, name='upload-f'),
    path('upload-d', views.upload_directory, name='upload-d'),
]