from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('/computers', views.computerManagements, name='computers-management'),
]