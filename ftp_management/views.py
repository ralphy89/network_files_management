from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
import os
from . import services

root = "C:\LAB-PROJECTs\\network_files_management\media\\"
host_ = 'LAB-C113'
password_ = 'LAB-C113'
global DEVICES
DEVICES = []
# Create your views here.

def home(request):
    template = 'home.html'
    global DEVICES
    if len(DEVICES) == 0:
        DEVICES = services.get_devices() # [['name', 'ip', 'mac'], ..., ...]
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

def files_management(request):
    global DEVICES

    template = 'gestionnaire_fichiers/file_management.html'
    if len(DEVICES) == 0:
        DEVICES = services.get_devices()

    page_object = {}
    assert template == 'gestionnaire_fichiers/file_management.html', 'template should be \"gestionnaire_fichiers/file_management.html\"'
    return render(
        request,
        template,
        page_object,
    )

@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files[]')  # Access the array of files
        saved_files = []
        for file in files:
            file_path = default_storage.save(f'uploads/{file.name}', file)
            saved_files.append(f"{root}{file_path}")
        print('Sharing files .... ')
        hosts = transfer_files(saved_files)
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
                return JsonResponse({'status': 'error', 'message': 'Invalid directory root.'})
            saved_files.append(directory_root)

        hosts = transfer_files(saved_files, True)
        return JsonResponse({'status': 'success', 'files': saved_files, 'hosts': hosts})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})



def transfer_files(paths, r=False):
    hosts = {'ips': []}
    try:
        for ip in DEVICES: # [['name', 'ip', 'mac'], ..., ...]

            for path in paths:
                # services.ssh_copy_file_to_remote_client(host_, ip[1], password_, path, r)
                print(f"Sharing to {host_}@{ip[1]} : {path}")
            hosts['ips'].append(ip[1])
        print(f'Hosts : {hosts}')
        return hosts
    except Exception as e:
        print(f'Error sharing files : {e}')


