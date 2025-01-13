from django.shortcuts import render
from .models import Computer, Student
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
django_admin_page_info = ('89zone', 'admin-password')

# Create your views here.

def computerManagements(request):
    template = 'computerManagement.html'

    computers = Computer.objects.all().values()
    students = Student.objects.all().values()
    print(students)
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
            computer=computer
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
        if POST_data['status'] == 'Active':
            student.status = 'Inactive'
            computer.student_assigned = None
            computer.status = 'Available'
        else:
            student.status = 'Active'
            infos = {
                'email': student.email + ' - ' + student.code,
                'name' : student.name
            }
            computer.student_assigned = infos
            computer.status = 'Occupied'
        computer.save()
        student.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
