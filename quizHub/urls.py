from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('quizHub', views.quizHub, name='quizHub'),
    path('quizHub/prepareQuiz/<int:quiz_id>/edit/<str:title>', views.prepareQuiz, name='prepareQuiz'),
    path('prepareQuiz', views.prepareQuiz, name='prepareQuiz'),
    path('publishQuiz', views.publishQuiz, name='publishQuiz'),
    path('quizHub/addQuestion/to/<int:quiz_id>/', views.addQuestion, name='addQuestion'),
    path('login-page-quizHub', views.login_page_quizHub, name='login-page-quizHub'),
    path('sendResults', views.sendResults, name='sendResults'),
    path('logout-quizHub', views.logout, name='logout-quizHub'),
    path('createAccount', views.createAccount,name='createAccount'),
    path('quizHubStudent', views.quizHubStudent, name='quizHubStudent'),
    path('takeQuiz/<int:quiz_id>/<str:title>', views.takeQuiz, name='takeQuiz'),
    path('submitQuiz', views.submitQuiz, name='submitQuiz'),
    path('seeSubmissions/<int:quiz_id>', views.seeSubmissions, name='seeSubmissions')
]