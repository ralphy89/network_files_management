from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('quizHub', views.quizHub, name='quizHub'),
    path('quizHub/prepareQuiz/<int:quiz_id>/edit/<str:title>', views.prepareQuiz, name='prepareQuiz'),
    path('prepareQuiz', views.prepareQuiz, name='prepareQuiz'),
    path('quizHub/addQuestion/to/<int:quiz_id>/', views.addQuestion, name='addQuestion'),
    path('login-page-quizHub', views.login_page_quizHub, name='login-page-quizHub')
]