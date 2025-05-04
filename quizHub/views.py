from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .models import Quiz, Question, MultipleChoiceAnswer, ShortAnswer, Submission, SubmissionAnswer
from django.utils import timezone
import json
import datetime
import threading
PUBLISHED_QUIZ = list()
HT_TIME_DELTA = datetime.timedelta()
HT_TZ_OBJECT = datetime.timezone(HT_TIME_DELTA,
                               name="UTC")

def isTeacher(request):
    if request.user.is_authenticated:
        types = str(request.user.groups.all().values())
        if 'Teacher' in types:
            return True
    return False
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
        "type": type,
        'creatingAccount': False,
    }
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        types = ''
        valid_user = authenticate(request, username=email, password=password)
        if valid_user is not None:
            login(request, valid_user)
            if len(valid_user.groups.all()):
                types = str(valid_user.groups.all().values())

        # messages.success(request, f"Login {type} Successfully")
            if 'Teacher' in types:
                return redirect(to='quizHub')
            else:
                return redirect(to='quizHubStudent')
        else:
            messages.error(request, "Incorrect email or password")

    return render(
                request,
                template,
                page_object,
            )


@login_required(login_url='login-page-quizHub')
def logout(request):
    auth_logout(request)
    return render(
        request,
        'login-page.html',
    )
@csrf_exempt
def createAccount(request):

    template = 'login-page.html'
    if request.method == 'GET':
        page_object = {
            'creatingAccount': True,
        }
        return render(
            request,
            template,
            page_object,
        )
    elif request.method == 'POST':
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']

        try:
            user = User.objects.create_user(username=email, email=email,
                                            password=password, first_name=firstname,
                                            last_name=lastname)
            user.groups.add(2)
            valid_user = authenticate(request, username=email, password=password)
            if valid_user is not None:
                login(request, valid_user)
                if len(valid_user.groups.all()):
                    types = str(valid_user.groups.all().values())
        
                # messages.success(request, f"Login {type} Successfully")
                if 'Teacher' in types:
                    return redirect(to='quizHub')
                else:
                    return redirect(to='quizHubStudent')

        
            return render(
                request,
                template,
                page_object,
            )
        except Exception as e:
            if str(email) in str(e):
                messages.error(request, "Email already exist")
            else:
                messages.error(request, 'Please, contact the administrator!')

        return redirect('createAccount')

@login_required(login_url='login-page-quizHub')
def quizHub(request):
    template = 'quiz-home.html'
    email = ''
    password = ''
    type = 'Student'

    valid_user = request.user
    if valid_user.is_authenticated:

        if len(valid_user.groups.all()):
            types = list(valid_user.groups.all().values())[-1]['name']
            if 'Student' in types:
                return  redirect('quizHubStudent')

        quiz_list = Quiz.objects.filter(author=valid_user)
        questions = []
        answers = []
        for quiz in quiz_list:

            for question in quiz.question_set.all():
                if question.question_type == 'MC':
                    answers = answers + list(question.get_answers())


            questions = questions + list(quiz.question_set.all())
        page_object = {

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
def quizHubStudent(request):
    template = 'quiz-home.html'
    email = ''
    password = ''
    valid_user = request.user
    if valid_user.is_authenticated:
        if len(valid_user.groups.all()):
            types = str(valid_user.groups.all())
        if 'Student' in types:
            quiz_list = Quiz.objects.filter(status='P')
            submission_list = Submission.objects.filter(student=request.user)
            questions = []
            answers = []
            if len(quiz_list) > 0:
                for quiz in quiz_list:
                    for question in quiz.question_set.all():
                        if question.question_type == 'MC':
                            answers = answers + list(question.get_answers())
                    questions = questions + list(quiz.question_set.all())

            page_object = {

                'quiz_list': quiz_list,
                'submission_list':submission_list,
                'questions': questions,
                'answers': answers,
            }
            return render(
                request,
                template,
                page_object,
            )



def endQuiz (quizId, quizTitle):
    quiz = Quiz.objects.get(quiz_id=quizId, title=quizTitle)
    if quiz:
        quiz.status = 'A'
        # sendNotification
        quiz.save()
        PUBLISHED_QUIZ.remove(quiz)
        print(f"\nTime's Over\nQuiz {quiz.quiz_id} - {quiz.title} Archived!")
    return

@login_required(login_url='login-page-quizHub')
def sendResults(request):
    if isTeacher(request):
        if request.method == 'POST':
            quizId = json.loads(request.body)['quiz_id']
            quiz = Quiz.objects.get(quiz_id=quizId)
            quiz.is_corrected = True
            print("Student get their result!")
            # quiz.save()
            return JsonResponse({'status': 'success', 'message': 'Student get theirs results'})

def startQuiz (quizId, quizTitle):
    quiz = Quiz.objects.get(quiz_id=quizId, title=quizTitle)
    if quiz:
        quiz.status = 'P'
        # sendNotification
        quiz.save()

        PUBLISHED_QUIZ.append(quiz)
        end_quiz_thread = threading.Timer(interval=float(quiz.duration * 60), function= endQuiz, args=(quiz.quiz_id, quiz.title))
        end_quiz_thread.start()
    return
@login_required(login_url='login-page-quizHub')
def publishQuiz(request):
    if isTeacher(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            quiz = Quiz.objects.get(quiz_id=data['quiz_id'], title=data['quiz_title'])
            if quiz:
                quiz.duration = int(data['duration']) + 2
                quiz.start = datetime.datetime.now()
                quiz.status = 'P'
                if 'scheduled_datetime' in data:
                    date_t = datetime.datetime.fromisoformat(data['scheduled_datetime'])
                    quiz.start = date_t
                    quiz.status = 'S'
                    end_time = quiz.start + datetime.timedelta(minutes=quiz.duration)
                    second_between_now_start = quiz.start.astimezone(HT_TZ_OBJECT) - datetime.datetime.now().astimezone(HT_TZ_OBJECT)
                    print(f"Quiz {quiz.quiz_id} - {quiz.title} scheduled now : {quiz.start}."
                          f"\nWill Archived {end_time}")
                    start_quiz_thread = threading.Timer(interval=float(second_between_now_start.total_seconds()), function= startQuiz, args=(quiz.quiz_id, quiz.title))
                    start_quiz_thread.start()
                else :
                    PUBLISHED_QUIZ.append(quiz)
                    end_time = quiz.start + datetime.timedelta(minutes=quiz.duration)
                    print(f"Quiz {quiz.quiz_id} - {quiz.title} start now for a duration of {quiz.duration} mins."
                          f"\nWill Archived {end_time}")
                    end_quiz_thread = threading.Timer(interval=float(quiz.duration * 60), function= endQuiz, args=(quiz.quiz_id, quiz.title))
                    end_quiz_thread.start()
                quiz.save()

                return JsonResponse({'status': 'success', 'message': 'Quiz Published Successfully'})
    return JsonResponse({'status': 'error', 'message': 'Request failed'})


@login_required(login_url='login-page-quizHub')
def takeQuiz(request, quiz_id:int = None, title:str = None):
    def setTimezone(arg: datetime):
        result = arg.astimezone(HT_TZ_OBJECT)
        return result.strftime('%Y-%m-%d %H:%M')

    template = 'quizTemplate.html'

    if request.method == 'GET':

        quiz = Quiz.objects.get(quiz_id=quiz_id)
        if quiz.status in ['D', 'S']:
            return JsonResponse({'status': 'Warning', 'message': 'You don\'t have access to this page'})

        isAlreadySubmit = list(Submission.objects.filter(quiz=quiz, student=request.user))
        submission_answers = SubmissionAnswer.objects.filter(submission=isAlreadySubmit[0]) if len(isAlreadySubmit) != 0 else list()
    # "2025-03-08 14:30"
        page_object = {
            'quiz_id': quiz_id,
            'quiz_title':title,
            'quiz_description':quiz.description,
            'questions':quiz.question_set.all(),
            'quiz_status': quiz.status,
            'quiz_duration': quiz.duration - 2,
            'quiz_start': setTimezone(quiz.start),
            'submitted': True if len(isAlreadySubmit) != 0 else False,
            'submission_answers': list(submission_answers),
        }

        return render(
            request,
            template,
            page_object,
        )

    return JsonResponse({'status': 'Warning', 'message': 'You don\'t have access to this page'})

@login_required(login_url='login-page-quizHub')
def submitQuiz(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        quiz = Quiz.objects.get(quiz_id=data['quiz_id'], title=data['quiz_title'])
        if quiz.status in ['D', 'S', 'A']:
            return JsonResponse({'status': 'Warning', 'message': 'Too late!!'})

        isAlreadySubmit = list(Submission.objects.filter(quiz=quiz, student=request.user))
        if quiz and (len(isAlreadySubmit) == 0):

            # check if late
            submission = Submission(
                quiz= quiz,
                student=request.user,
            )
            submission.save()
            score = 0.0
            student_answer = None
            student = request.user.username
            answers = list(json.loads(data['answers']))

            for answer in answers:
                quiz_question = Question.objects.get(question_id=answer['question_id'])
                submissionAnswer = None
                if answer['type'] == 'MC':
                    MCA = MultipleChoiceAnswer.objects.get(id=answer['answer'])
                    if MCA.is_correct:
                        score += quiz_question.points
                    submissionAnswer = SubmissionAnswer(
                        submission=submission,
                        mca=MCA
                    )
                elif answer['type'] == 'SA':
                    quiz_question = Question.objects.get(question_id=answer['question_id'])
                    getSA = ShortAnswer.objects.get(id=answer['answer'])

                    submissionAnswer = SubmissionAnswer(
                        submission=submission,
                        sa=getSA
                    )
                submissionAnswer.save()
            submission.score = score
            submission.save()
            quiz.submissions += 1
            quiz.save()
            return JsonResponse({'status': 'success', 'message': 'Quiz submitted successfully'})
    return JsonResponse({'status': 'error', 'message': 'Quiz has\'nt been submitted'})



@csrf_exempt
@login_required(login_url='login-page-quizHub')
def prepareQuiz(request, quiz_id:int = None, title:str = None):
    if isTeacher(request):
        def setTimezone(arg: datetime):
            result = arg.astimezone(HT_TZ_OBJECT)
            return result.strftime('%Y-%m-%d %H:%M')

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
            'quiz_title':quiz.title,
            'quiz_description':quiz.description,
            'quiz_status': quiz.status,
        }

        return render(
            request,
            template,
            page_object,
        )

    elif request.method == 'GET':
        quiz = Quiz.objects.get(quiz_id=quiz_id)
        # "2025-03-08 14:30"
        page_object = {
            'quiz_id': quiz_id,
            'quiz_title':title,
            'quiz_description':quiz.description,
            'questions':quiz.question_set.all(),
            'quiz_status': quiz.status,
            'quiz_duration': quiz.duration - 2,
            'quiz_start': setTimezone(quiz.start),
        }

        return render(
            request,
            template,
            page_object,
        )

    return JsonResponse({'status': 'Warning', 'message': 'You don\'t have access to this page'})


@login_required(login_url='login-page-quizHub')
def addQuestion(request, quiz_id):
    if isTeacher(request):
        if request.method == 'POST':
            question = json.loads(request.body)
            quiz = Quiz.objects.get(quiz_id=quiz_id)
            new_question = Question(question_text=str(question['text']).strip(), question_type=question['type'],
                                    points=question['points'], quiz=quiz)

            new_question.save()
            quiz.total_point += int(new_question.points)
            quiz.save()
            if new_question.question_type == 'MC':
                for answer in question['answers']:
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


@login_required(login_url='login-page-quizHub')
def seeSubmissions (request, quiz_id:int = None):
    template = 'submissions.html'
    valid_user = request.user
    if 'Teacher' in str(valid_user.groups.all()):
        submissions = Submission.objects.filter(quiz_id=quiz_id)

        quiz = Quiz.objects.get(quiz_id=quiz_id)
        submissions_answers = SubmissionAnswer.objects.filter(submission__quiz=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        page_object = {
            'submissions':submissions if len(submissions) > 0 else [],
            'quiz': quiz,
            'questions':questions,
            'submission_answers': submissions_answers,
        }

        return render(
            request,
            template,
            page_object,
        )
    else :
        return JsonResponse({'status': 'Warning', 'message': 'You don\'t have access to this page'})


