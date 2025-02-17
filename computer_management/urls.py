from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('computers', views.computerManagements, name='computers-management'),
    path('add-computer', views.addComputer, name='add-computer'),
    path('edit-computer', views.editComputer, name='edit-computer'),

    path('add-student', views.addStudent, name='add-student'),
    path('get-student', views.get_student, name='get-student'),
    path('update-student-status', views.updateStudentStatus, name='change-student-status'),
    path('update-student', views.updateStudent, name='update-student'),
    path('get-histories', views.get_histories, name='histories-by-name'),
    path('search-student', views.searchStudent, name='search-student'),
    path('guests', views.guests_management, name='guests-management'),
    path('schedules', views.scheduleManagements, name='schedules-management'),
    path('add-schedule', views.addSchedule, name='add-schedule'),
    path('update-schedule', views.updateSchedule, name='update-schedule'),

    path('get-schedule', views.get_schedule, name='get-schedule'),
    path('check-schedule', views.checkSchedule, name='check-schedule'),


]