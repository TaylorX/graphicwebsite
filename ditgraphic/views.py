from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader, Context

def index(request):
    return render(request,"Sites/index.html",{'contact':'contact'})

def ExecutionTime(request):
    return render(request,"Sites/execution_time.html",{'contact':'contact'})