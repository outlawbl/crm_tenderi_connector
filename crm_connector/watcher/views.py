from django.http import HttpResponse
from django.shortcuts import render
from flask import render_template
from httplib2 import Http

# Create your views here.
def test(request):
    print('test radi')
    return HttpResponse('dugme kliknuto')

def home(request):
    print('dugme kliknuto')
    return render(request ,'watcher/home.html')