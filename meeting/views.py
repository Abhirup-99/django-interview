from django.http.response import JsonResponse
from django.shortcuts import render


def index(request):
    return render(request,'index.html')

def submitForm(request):
    return JsonResponse({'status':'sucess'})