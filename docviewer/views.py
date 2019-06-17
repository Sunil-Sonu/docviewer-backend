from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from docviewer.models import *

import requests
import json
import uuid

@csrf_exempt
def getFiles(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Please login'}, status=401)
    filePath = request.GET['path'] if 'path' in request.GET else ""
    response = requests.post('https://api.dropboxapi.com/2/files/list_folder', headers= {'Authorization': 'Bearer w3mybzDx2AAAAAAAAAAAp-dAkpeDk9G1Mnh_Ze3-latb8lXZwNpudRkuRaTztegp', 'Content-Type': 'application/json'}, data=json.dumps({
    "path": UserFolder.objects.get(creator=request.user).folderPath + filePath,
    "recursive": False,
    "include_media_info": False,
    "include_deleted": False,
    "include_has_explicit_shared_members": False,
    "include_mounted_folders": True,
    "include_non_downloadable_files": True
}))
    return JsonResponse(response.json(), content_type = 'application/json')

@csrf_exempt
def getDownloadLink(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Please login'}, status=401)
    filePath = request.GET['path']
    response = requests.post('https://api.dropboxapi.com/2/files/get_temporary_link', headers= {'Authorization': 'Bearer w3mybzDx2AAAAAAAAAAAp-dAkpeDk9G1Mnh_Ze3-latb8lXZwNpudRkuRaTztegp', 'Content-Type': 'application/json'}, data=json.dumps({
        "path": UserFolder.objects.get(creator=request.user).folderPath + filePath
    }))
    return JsonResponse(response.json(), content_type = 'application/json')

@csrf_exempt
def uploadFile(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Please login'}, status=401)
    file = request.FILES.getlist('fileData')
    filePath = path = request.POST['path'] if 'path' in request.GET else ""
    fs = FileSystemStorage(location='/media')
    file_name = fs.save(file.name, file)
    # TODO: Implement reading the file and uploading it.
    response = requests.post('https://content.dropboxapi.com/2/files/upload', headers= {'Authorization': 'Bearer w3mybzDx2AAAAAAAAAAAp-dAkpeDk9G1Mnh_Ze3-latb8lXZwNpudRkuRaTztegp', 
    'Dropbox-API-Arg': '{\"path\": ' + UserFolder.objects.get(creator=request.user).folderPath + filePath + ',\"mode\": \"add\",\"autorename\": true,\"mute\": false,\"strict_conflict\": false}"',
        'Content-Type': 'application/octet-stream'}, 
        data=file)
    return JsonResponse({'success': file_name}, content_type = 'application/json')

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return JsonResponse({'data': 'Success'}, content_type = 'application/json')
            else:
                return JsonResponse({'error_message': 'Your account is disabled.'}, status= 401)
        else:
            return JsonResponse({'error_message': 'Invalid Login Details'}, status= 401)
    return JsonResponse({'error_message': 'Invalid Login Request'}, status= 500)

@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username is None or email is None or password is None:
            return JsonResponse({'error_message': 'Please enter proper details'}, status=400)
        user = User.objects.create_user(username = username, email = email, password = password)
        if user:
            response = requests.post('https://api.dropboxapi.com/2/files/create_folder_v2', headers= {'Authorization': 'Bearer w3mybzDx2AAAAAAAAAAAp-dAkpeDk9G1Mnh_Ze3-latb8lXZwNpudRkuRaTztegp', 'Content-Type': 'application/json'}, data=json.dumps({
            "path": "/" + uuid.uuid4().hex,
            "autorename": False
            }))
            if response.status_code == 200:
                UserFolder.objects.create(folderId=response.json()['metadata']['id'], creator=user, folderPath=response.json()['metadata']['path_display'])
                return JsonResponse({'message': 'Success'})
            else:
                user.delete()
    return JsonResponse({'error_message': 'Not a valid request'}, status=500)