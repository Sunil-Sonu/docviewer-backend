from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt
from docviewer import views

def getRoutes():
    return [
        re_path(r'getFiles$', views.getFiles, name = 'getFiles'),
        re_path(r'getDownloadLink$', views.getDownloadLink, name = 'getDownloadLink'),
        re_path(r'uploadFile$', views.uploadFile, name = 'uploadFile'),
        re_path(r'login$', views.user_login, name = 'login'),
        re_path(r'signup$', views.user_register, name = 'signup'),
    ];