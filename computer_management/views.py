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
        histories_list = DateTimeEncoder().encode(histories)
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
    return JsonResponse({'status': 'success', 'student': student})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def addComputer(request):

    if request.method == 'POST':
        POST_data = json.loads(request.POST['computer'])
        computer = Computer(name=POST_data['name'], mac_adr=POST_data['mac'],
                            status=POST_data['status'], computer_position=POST_data['position'])
        computer.save()
        computers_list = DateTimeEncoder().encode(list(Computer.objects.all().values()))
        return JsonResponse({'status': 'success', 'computers': computers_list})


@csrf_exempt
def editComputer(request):
    if request.method == 'POST':
        POST_data = json.loads(request.POST['computer'])
        computer = Computer.objects.get(name=POST_data['name'])
        if computer:
            computer.computer_position = POST_data['position']
            computer.save()
            return JsonResponse({'status': 'success', 'message': 'Computer edited!'})
        return JsonResponse({'status': 'error', 'message': 'Computer not found!.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@csrf_exempt
def addStudent(request):
    if request.method == 'POST':
        POST_data = json.loads(request.POST['student'])
        computer = Computer.objects.get(name=POST_data['computer'])
        name = str(POST_data['name']).lower().split()
        new_name = ''
        for n in name:
            new_name += f"{n.capitalize()} "
        name = new_name.strip()
        student = Student(
            name=name,
            code=str(POST_data['code']).upper(),
            email=str(POST_data['email']).lower(),
            status='Inactive',
            computer=computer,
            option=POST_data['option']
        )
        student.save()

        # if POST_data['status'] == 'Active':
        #     infos = {
        #         'email': POST_data['email'] + ' - ' + POST_data['code'],
        #         'name' : POST_data['name']
        #     }
            # history = History(
            #     student= student,
            #     computer= computer,
            #     title=f'{student.code} used {computer.name}',
            #     description=POST_data['comment'],
            # )
            # history.save()
            # student.curr_hist_id = history.history_id
            # computer.student_assigned = infos
            # computer.status = 'Occupied'
            # computer.save()
        students_list = DateTimeEncoder().encode(list(Student.objects.all().values()))
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
            if computer.status != 'Occupied' and computer.status != 'Maintenance':
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
            else :
                return JsonResponse({'status': 'Warning', 'message': 'Computer status : ' + computer.status})

        computer.save()
        student.save()

        return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def updateStudent(request):
    if request.method == 'POST':
        POST_data = json.loads(request.POST['student'])
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

@csrf_exempt
def searchStudent(request):
    if request.method == 'POST':
        POST_data = str(json.loads(request.POST['query'])['arg']).strip()
        result = None
        if len(POST_data) > 0:
            result = Student.objects.filter(name__regex=POST_data)
            if (len(result) == 0):
                result = Student.objects.filter(email__regex=POST_data)
                if (len(result) == 0):
                    result = Student.objects.filter(code__regex=POST_data)
                    if len(result) == 0:
                        result = Student.objects.filter(computer__name__regex=POST_data)

        if result != None:
            result = DateTimeEncoder().encode(list(result.values()))
            return JsonResponse({'status': 'success', 'result': result})
        else:
            return JsonResponse({'status': 'success', 'message': 'no result'})


    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


