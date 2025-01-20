from django.shortcuts import render
from .models import Computer, Student, History
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import datetime
from datetime import timezone
django_admin_page_info = ('89zone', 'admin-password')
# subclass JSONEncoder
class DateTimeEncoder(json.JSONEncoder):
    #Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
# Create your views here.

def computerManagements(request):
    template = 'computerManagement.html'

    computers = Computer.objects.all().values()
    students = Student.objects.all().values()
    page_object = {
        'computers': computers,
        'students': students,
    }
    assert template == 'computerManagement.html', 'template should be \"computerManagement.html\"'
    return render(
        request,
        template,
        page_object,
    )

@csrf_exempt
def get_histories(request):
    if request.method == 'POST':
        POST_data = json.loads(request.POST['name'])['name']
        histories = list(History.objects.filter(computer__name=POST_data).values())
        histories_list = json.dumps(DateTimeEncoder().encode(histories))
        return JsonResponse({'status': 'success', 'histories': histories_list})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def get_student(request):
    if request.method == 'POST':
        POST_data = json.loads(request.POST['student'])['code']
        result = Student.objects.get(code=POST_data).__dict__
        to_pop = ['_state', 'student_id', 'curr_hist_id', 'student_history',
                'created', 'updated']
        for item in to_pop:
            result.pop(item)
        student = DateTimeEncoder().encode(result)

        print(student)
    return JsonResponse({'status': 'success', 'student': student})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def addComputer(request):

    if request.method == 'POST':
        POST_data = json.loads(request.POST['computer'])
        computer = Computer(name=POST_data['name'], mac_adr=POST_data['mac'], status=POST_data['status'])
        computer.save()
        computers_list = json.dumps(list(Computer.objects.all().values()))
        return JsonResponse({'status': 'success', 'computers': computers_list})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def addStudent(request):
    if request.method == 'POST':
        POST_data = json.loads(request.POST['student'])
        computer = Computer.objects.get(name=POST_data['computer'])


        if POST_data['status'] == 'Active':
            infos = {
                'email': POST_data['email'] + ' - ' + POST_data['code'],
                'name' : POST_data['name']
            }
            computer.student_assigned = infos
            computer.status = 'Occupied'
            computer.save()

        student = Student(
            name=POST_data['name'],
            code=POST_data['code'],
            email=POST_data['email'],
            status=POST_data['status'],
            computer=computer,
            option=POST_data['option']
        )

        student.save()
        students_list = json.dumps(list(Student.objects.all().values()))
        return JsonResponse({'status': 'success', 'students': students_list})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def updateStudentStatus(request):
    if request.method == 'POST':
        POST_data = json.loads(request.POST['update'])
        student = Student.objects.get(code=POST_data['code'])
        computer = Computer.objects.get(name=student.computer_id)
        history = None
        if POST_data['status'] == 'Active':
            history = History.objects.get(history_id=student.curr_hist_id)
            history.end_date = datetime.datetime.now(timezone.utc)
            student.status = 'Inactive'
            computer.student_assigned = None
            computer.status = 'Available'
            student.curr_hist_id = None
            student.student_history = history.end_date
            history.save()
        else:
            student.status = 'Active'
            infos = {
                'email': student.email + ' - ' + student.code,
                'name' : student.name
            }
            computer.student_assigned = infos
            computer.status = 'Occupied'
            history = History(
                student= student,
                computer= computer,
                title=f'{student.code} used {computer.name}',
                description=POST_data['comment'],
            )
            history.save()
            student.curr_hist_id = history.history_id

        computer.save()
        student.save()

        return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def updateStudent(request):
    if request.method == 'POST':
        POST_data = json.loads(request.POST['student'])
        print(POST_data)
        code = POST_data['prev_code']
        student = Student.objects.get(code=code)
        computer = Computer.objects.get(name=POST_data['computer'])
        student.name = POST_data['name']
        if (code != POST_data['code']) :
            student.code = POST_data['code']
        student.email = POST_data['email']
        student.option = POST_data['option']
        student.computer = computer
        student.save()
    return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
