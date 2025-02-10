from django.shortcuts import render
from django.db.models import Q
from .models import Computer, Student, History, Schedule
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
        if isinstance(obj, (datetime.date, datetime.datetime, datetime.time)):
            return obj.isoformat()
# Create your views here.

def computerManagements(request):
    template = 'computerManagement.html'

    computers = Computer.objects.all().values()
    students = Student.objects.filter(type='Student').values()
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

def scheduleManagements(request):
    template = 'scheduleManagement.html'

    schedules = Schedule.objects.all().values()
    computers = Computer.objects.all().values()
    students = Student.objects.all().values()

    page_object = {
        'schedules': schedules,
        'computers': computers,
        'students': students,
    }
    assert template == 'scheduleManagement.html', 'template should be \"scheduleManagement.html\"'
    return render(
        request,
        template,
        page_object,
    )
def guests_management(request):
    template = 'guestsManagement.html'

    computers = Computer.objects.all().values()
    students = Student.objects.filter(type='Guest').values()
    page_object = {
        'computers': computers,
        'students': students,
    }
    assert template == 'guestsManagement.html', 'template should be \"guestsManagement.html\"'
    return render(
        request,
        template,
        page_object,
    )

def hasConflict(day, s_hour_, e_hour_, student_, computer_, id_to_exclude):
    registered_for_given_day = None
    if id_to_exclude == None:
        registered_for_given_day = Schedule.objects.filter(day=day).values()
    else:
        registered_for_given_day = Schedule.objects.filter(day=day).exclude(schedule_id=id_to_exclude).values()

    if len(registered_for_given_day) > 0 :
        registered_for_given_computer = registered_for_given_day.filter(computer_id=computer_)
        if len(registered_for_given_computer) > 0:
            conflict_list = registered_for_given_computer.filter(
                (Q(end_hour__gte=e_hour_) & Q(start_hour__lte=e_hour_)) |
                (Q(end_hour__gte=s_hour_) & Q(start_hour__lte=s_hour_))
            )
            if len(conflict_list) == 0:
                return False
            else:
                return True

    return False


@csrf_exempt
def addSchedule(request):
    if request.method == 'POST':
        POST_data = json.loads(request.POST['schedule'])
        student = Student.objects.get(code=POST_data['student'])
        computer = Computer.objects.get(name=POST_data['computer'])

        s_hour = datetime.time(POST_data['s_hour'])
        e_hour = datetime.time(POST_data['e_hour'])
        day = POST_data['day']
        hasConflict_ = hasConflict(day, s_hour, e_hour, student.code, computer.name, None)
        if(not hasConflict_):
            schedule = Schedule(day=day, start_hour=s_hour, end_hour=e_hour,
                                student=student, computer=computer)
            schedule.save()

            return JsonResponse({'status': 'success', 'message':'Schedule added Successfully!'})
        else:
            return JsonResponse({'status': 'warning', 'message':'Schedule Conflict detected!!!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def updateSchedule(request):
    if request.method == 'POST':
        POST_data = json.loads(request.POST['schedule'])
        schedule = Schedule.objects.get(schedule_id=POST_data['prev_code'])
        student = Student.objects.get(code=POST_data['student'])
        computer = Computer.objects.get(name=POST_data['computer'])

        s_hour = datetime.time(POST_data['s_hour'])
        e_hour = datetime.time(POST_data['e_hour'])
        day = POST_data['day']
        hasConflict_ = hasConflict(day, s_hour, e_hour, student.code, computer.name, POST_data['prev_code'])
        if(not hasConflict_):
            schedule.day=day
            schedule.start_hour=s_hour
            schedule.end_hour=e_hour
            schedule.student=student
            schedule.computer=computer
            schedule.save()
            return JsonResponse({'status': 'success', 'message':'Schedule updated Successfully!'})
        else:
            return JsonResponse({'status': 'warning', 'message':'Schedule Conflict detected!!!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def get_schedule(request):
    if request.method == 'POST':
        POST_data = json.loads(request.POST['schedule'])['schedule_id']
        result = Schedule.objects.get(schedule_id=POST_data).__dict__
        to_pop = ['created', 'updated']
        for item in to_pop:
            result.pop(item)
        schedule = DateTimeEncoder().encode(result)
    return JsonResponse({'status': 'success', 'schedule': schedule})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def checkSchedule(request):
    if request.method == 'POST':
        POST_data = json.loads(request.POST['schedule'])
        computer = Computer.objects.get(name=POST_data['computer'])

        s_hour = datetime.time(POST_data['s_hour'])
        e_hour = datetime.time(POST_data['e_hour'])
        day = POST_data['day']
        hasConflict_ = hasConflict(day, s_hour, e_hour, '', computer.name, None)
        if(not hasConflict_):
            return JsonResponse({'status': 'success', 'message':f'{computer} is Available for this schedule!'})
        else:
            return JsonResponse({'status': 'warning', 'message':'Schedule Conflict detected!!!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

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
        print(POST_data)
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
            option=POST_data['option'],
            type=POST_data['type'],
            phone= POST_data['phone']
        )

        if student.code == 'GUEST':
            student.code += f'-{student.email}'

        student.save()
        print(student)
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
                student.number_of_uses += 1
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
        if student.computer.name != computer.name:
            student.number_of_uses = 0;
            # CreateHistory()
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


