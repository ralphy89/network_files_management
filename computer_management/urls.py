from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('computers', views.computerManagements, name='computers-management'),
    path('add-computer', views.addComputer, name='add-computer'),
    path('add-student', views.addStudent, name='add-student'),
    path('get-student', views.get_student, name='get-student'),
    path('update-student-status', views.updateStudentStatus, name='change-student-status'),
    path('update-student', views.updateStudent, name='update-student'),
    path('get-histories', views.get_histories, name='histories-by-name'),
    path('search-student', views.searchStudent, name='search-student'),
]