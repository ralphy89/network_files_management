from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from .models import Quiz, Question, MultipleChoiceAnswer, ShortAnswer
from django.utils import timezone
import json
import datetime

# Create your views here.

class DateTimeEncoder(json.JSONEncoder):
    #Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime, datetime.time)):
            return obj.isoformat()
@csrf_exempt
def login_page_quizHub(request):
    template = 'login-page.html'

    email = ''
    password = ''
    type = 'Student'
    page_object = {
        "type": type
    }
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        valid_user = authenticate(request, username=email, password=password)
        if valid_user is not None:
            login(request, valid_user)
            if len(valid_user.groups.all()):
                type = list(valid_user.groups.all().values())[-1]['name']

        # messages.success(request, f"Login {type} Successfully")
            if type == 'Teacher':
                return redirect(to='quizHub')
            if type == 'Student':
                return redirect(to='quizHub')
        else:
            messages.error(request, "Incorrect email or password")

    return render(
                request,
                template,
                page_object,
            )

@login_required(login_url='login-page-quizHub')
@csrf_exempt
def quizHub(request):
    template = 'quiz-home.html'
    email = ''
    password = ''
    type = 'Student'

    valid_user = request.user
    if valid_user.is_authenticated:

        if len(valid_user.groups.all()):
            type = list(valid_user.groups.all().values())[-1]['name']

        quiz_list = Quiz.objects.filter(author=valid_user)
        questions = []
        answers = []
        for quiz in quiz_list:

            for question in quiz.question_set.all():
                if question.question_type == 'MC':
                    answers = answers + list(question.get_answers())
                

            questions = questions + list(quiz.question_set.all())
        page_object = {
            "user_type": type,
            'quiz_list': quiz_list,
            'questions': questions,
            'answers': answers,
        }
        return render(
            request,
            template,
            page_object,
        )

@login_required(login_url='login-page-quizHub')
@csrf_exempt
def prepareQuiz(request, quiz_id:int = None, title:str = None):
    template = 'quizTemplate.html'

    if request.method == 'POST':
        # get quiz title and description
        title = request.POST['title']
        desc = request.POST['description']

        quiz = Quiz(
            title=title,
            description=desc,
            author=request.user,
            status='D',  # Published
            start=timezone.now() + timezone.timedelta(days=1),  # Starts tomorrow
            duration=45,  # 45 minutes
        )
        quiz.save()
        page_object = {
            'quiz_id': quiz.quiz_id,
            'quiz_title':title,
            'quiz_description':desc
        }

        return render(
                request,
                template,
                page_object,
            )

    elif request.method == 'GET':
        quiz = Quiz.objects.get(quiz_id=quiz_id)
        page_object = {
            'quiz_id': quiz_id,
            'quiz_title':title,
            'quiz_description':quiz.description,
            'questions':quiz.question_set.all(),
        }
        return render(
            request,
            template,
            page_object,
        )

    return JsonResponse({'status': 'Warning', 'message': 'You don\'t have access to this page'})


@login_required(login_url='login-page-quizHub')
@csrf_exempt
def addQuestion(request, quiz_id):
    if request.method == 'POST':
        question = json.loads(request.body)
        quiz = Quiz.objects.get(quiz_id=quiz_id)
        new_question = Question(question_text=str(question['text']).strip(), question_type=question['type'],
                                points=question['points'], quiz=quiz)

        new_question.save()
        if new_question.question_type == 'MC':
            for answer in question['answers']:
                print(answer)
                if len(str(answer['text']).strip()) > 0 :
                    to_add = MultipleChoiceAnswer(question=new_question, text=answer['text'], is_correct=answer['isCorrect'])
                    to_add.save()
                else:
                    if len(str(answer['text']).strip()) <= 0 and answer['isCorrect']:
                        to_add = MultipleChoiceAnswer(question=new_question, text="Aucune", is_correct=answer['isCorrect'])
                        to_add.save()
        elif new_question.question_type == 'SA':
            to_add = ShortAnswer(question=new_question, correct_answer=new_question['answer'])
        questions = quiz.question_set.all()
        index = 0
        temp_dict = dict()
        dict_questions = dict()
        for q in questions :
            if q.question_type == 'MC':
                temp_dict[q.question_text] = list()
                temp_dict['type'] = 'MC'
                temp_dict['points'] = q.points
                for a in q.get_answers():
                    temp_dict[q.question_text].append({a.text:a.is_correct})
            dict_questions[index] = temp_dict
            index += 1
            temp_dict = dict()

        return JsonResponse({'status': 'success', 'message': 'Question Added Successfully', 'questions': json.dumps(dict_questions)})
    return JsonResponse({'status': 'Error', 'message': 'Error', 'question': ''})



