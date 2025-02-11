from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
import os
from . import services

root = "C:\\LAB-PROJECTs\\network_files_management\\media\\"
host_ = 'LAB-C113'
password_ = 'LAB-C113'
global DEVICES
DEVICES = list()
# Create your views here.

def home(request):
    template = 'home.html'
    global DEVICES
    if len(DEVICES) == 0:
        DEVICES = services.get_devices() # [['name', 'ip', 'mac'], ..., ...]
    if (len(DEVICES) > 0):
        connected_devices = len(DEVICES)
        page_object = {
            'connected_devices': connected_devices,
            'devices': DEVICES
        }
        assert template == 'home.html', 'template should be \"home.html\"'
        return render(
            request,
            template,
            page_object,
        )
    return HttpResponse("ERROR GETTING YOUR LOCAL IP ADDRESS, Please make sure you're connected to the network!")

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




@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files[]')  # Access the array of files
        saved_files = []
        for file in files:
            file_path = default_storage.save(f'uploads/{file.name}', file)
            saved_files.append(f"{root}{file_path}")
        print('Sharing files .... ')
        hosts = transfer_files(saved_files, False)
        return JsonResponse({'status': 'success', 'files': saved_files, 'hosts': hosts})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

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

        hosts = transfer_files(saved_files, True)
        return JsonResponse({'status': 'success', 'files': saved_files, 'hosts': hosts})

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
    try:
        temp_ip = ''
        DEVICES = services.get_devices()
        for ip in DEVICES: # [['name', 'ip', 'mac'], ..., ...]
            if checkMac(ip[2]):
                print(f"-----------------------------------------------------------------\n"
                      f"Sharing to {host_}@{ip[1]}")
                session = services.Session(host_, ip[1], password_)
                session.make_ssh_connection()
                createDirectoryIfNotExist(services.default_dest_folder, session)

                for path in paths:
                    temp_ip = session.copy_file_to_remote_client(path, r)
                if temp_ip == ip[1]:
                    hosts['ips'].append(temp_ip)
                session.close()
            else:
                print("Devices is not registered in LABC113");
        return hosts
    except Exception as e:
        print(f'Error sharing files : {e}')

def createDirectoryIfNotExist(fileName, session):
    try:
        print("Creating file if not exist ....\n")
        session.createFileDirectory(fileName, True)
    except Exception as e:
        print(f'Error creating file : {e}')




