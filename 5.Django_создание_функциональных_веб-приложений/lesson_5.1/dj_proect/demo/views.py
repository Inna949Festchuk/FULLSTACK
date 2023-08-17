import datetime
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse('Hello from django')

def time(request):
    curent_time = datetime.datetime.now().time()
    return HttpResponse(f'Time = {curent_time}')
