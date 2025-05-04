import time

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
import os
import threading
from datetime import datetime
from . import services

root = "C:\\LAB-PROJECTs\\network_files_management\\media\\"
host_ = 'LAB-C113'
password_ = 'LAB-C113'
global DEVICES
DEVICES = list()
# Create your views here.


interval = 10 * 60
def refresh():
    global DEVICES
    DEVICES = services.get_devices() # [['name', 'ip', 'mac'], ..., ...]
    print("Rescanning...")
    threading.Timer(interval, refresh).start()

 # Interval in seconds
#refresh()

@login_required(login_url='login-page')
def logout(request):
    auth_logout(request)
    return render(
        request,
        'login.html',
    )
@csrf_exempt
def home(request):
    html_pages = ['home.html', 'login.html']
    template = html_pages[1]
    user_name = ''
    password = ''

    if request.method == 'POST':

        user_name = request.POST['username']
        password = request.POST['password']
        valid_user = authenticate(request, username=user_name, password=password)

        if valid_user is not None:
            login(request, valid_user)
            template = html_pages[0]
            # messages.success(request, "Login Successfully")
        else:
            messages.error(request, "Incorrect username or password")

    if request.user.is_authenticated:
        template = html_pages[0]

    if template == 'home.html':
        global DEVICES
        if len(DEVICES) == 0:
            DEVICES = services.get_devices() # [['name', 'ip', 'mac'], ..., ...]
        if (len(DEVICES) > 0):
            connected_devices = len(DEVICES)
            page_object = {
                'connected_devices': connected_devices,
                'devices': DEVICES
            }
            return render(
                request,
                template,
                page_object,
            )
        return HttpResponse("ERROR GETTING YOUR LOCAL IP ADDRESS, Please make sure you're connected to the network!")
    else:
        return render(
            request,
            template,
        )

@login_required(login_url='login-page')
def files_management(request):
    page_object = {}
    global DEVICES
    template = 'gestionnaire_fichiers/file_management.html'
    if len(DEVICES) == 0:
        DEVICES = services.get_devices()
    if (len(DEVICES) > 0):
        assert template == 'gestionnaire_fichiers/file_management.html', 'template should be \"gestionnaire_fichiers/file_management.html\"'
        return render(
            request,
            template,
            page_object,
        )
    return HttpResponse("ERROR GETTING YOUR LOCAL IP ADDRESS, Please make sure you're connected to the network!")



@login_required(login_url='login-page')
@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files[]')  # Access the array of files
        saved_files = []
        for file in files:
            file_path = default_storage.save(f'uploads\\{file.name}', file)
            saved_files.append(f"{root}{file_path}")
        print('Sharing files .... ')
        hosts, failed = transfer_files(saved_files, False)
        return JsonResponse({'status': 'success', 'files': saved_files, 'hosts': hosts, 'failed': failed})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required(login_url='login-page')
@csrf_exempt
def upload_directory(request):
    saved_files = []
    if request.method == 'POST':
        # Retrieve the directory path from the request
        directories_root = request.POST.getlist('dirs[]')
        print(directories_root)
        for directory_root in directories_root:
            # Check if the directory exists and is valid
            if not directory_root or not os.path.exists(directory_root) or not os.path.isdir(directory_root):
                return JsonResponse({'status': 'error', 'message': 'Invalid directory root.', 'directory': directory_root})
            saved_files.append(directory_root)

        hosts, failed = transfer_files(saved_files, True)
        return JsonResponse({'status': 'success', 'files': saved_files, 'hosts': hosts, 'failed': failed})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


# session = services.Session(host_, '192.168.1.153', password_)
# session.make_ssh_connection()
# session.copy_file_to_remote_client('C:\\Users\\LABC113-Ressources\\TEST-28.txt', False)
# session.close()

def checkMac(mac):
    mac = mac.split(':')
    first_3 = mac[0:3]
    if first_3 == ['f4', 'c8', '8a']:
        return True
    return False
def transfer_files(paths, r=False):

    hosts = {'ips': []}
    failed = {'ips': []}
    try:
        temp_ip = ''
        DEVICES = services.get_devices()
        for ip in DEVICES: # [['name', 'ip', 'mac'], ..., ...]
            if checkMac(ip[2]):
                print(f"-----------------------------------------------------------------\n"
                      f"Sharing to {host_}@{ip[1]}")
                session = services.Session(host_, ip[1], password_)
                if(session.make_ssh_connection()):
                    createDirectoryIfNotExist(services.default_dest_folder, session)


                    temp_ip = session.copy_file_to_remote_client(paths, r)
                    if temp_ip == ip[1]:
                        hosts['ips'].append(temp_ip)
                else:
                    failed['ips'].append(ip[1])
                session.close()
            else:
                print("Devices is not registered in LABC113");

        return hosts, failed
    except Exception as e:
        print(f'Error sharing files : {e}')

def createDirectoryIfNotExist(fileName, session):
    try:
        print("Creating file if not exist ....\n")
        session.createFileDirectory(fileName, True)
    except Exception as e:
        print(f'Error creating file : {e}')




