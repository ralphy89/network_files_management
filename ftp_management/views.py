from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
import os
from . import services

host_ = 'LAB-C113'
password_ = 'LAB-C113'
ip_ = ['192.168.43.153', '192.168.1.147']
# Create your views here.

def home(request):
    template = 'home.html'
    page_object = {}
    assert template == 'home.html', 'template should be \"home.html\"'
    return render(
        request,
        template,
        page_object,
    )

def files_management(request):
    template = 'gestionnaire_fichiers/file_management.html'
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
            saved_files.append(file_path)

        services.ssh_connection(host_, ip_[0], password_)

        return JsonResponse({'status': 'success', 'files': saved_files})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def upload_directory(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files[]')  # Access all files
        print(files)
        saved_files = []
        for file in files:
            # Get the relative path (e.g., "subfolder/filename.txt")
            relative_path = file.name
            print(relative_path)
            # Save the file preserving the relative directory structure
            # save_path = os.path.join('uploads', relative_path)
            # absolute_path = default_storage.save(save_path, file)
            # saved_files.append(absolute_path)

        return JsonResponse({'status': 'success', 'files': saved_files})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

