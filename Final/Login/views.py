from asyncio.windows_events import NULL
from cProfile import Profile
from unicodedata import name
from urllib.request import Request
from django.shortcuts import render, redirect
from .models import User
# Create your views here.
def index(request):
    test = request.GET.get('check')
    cont = {
        'check' : test,
    }
    return render(request, 'loginPages/index.html', cont)

def signup(request):
    return render(request, 'loginPages/signup.html')

def add_user(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        user  = request.POST['user']
        pwd   = request.POST['pwd']
        image = request.FILES['img']
        # image = 'Final/static/profiles/' + request.POST['img']
        print(image)
        obj = User(fname=fname, lname=lname, profile=image, username=user, password=pwd)
        obj.save()
    return redirect('/')
