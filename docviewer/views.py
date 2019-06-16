from django.shortcuts import render
from django.http import JsonResponse


def getFiles(request):
    return JsonResponse('Implement Get Files method', content_type = 'application/json')
