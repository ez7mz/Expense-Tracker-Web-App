from asyncio.windows_events import NULL
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Login.models import User
from .models import Transaction
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
# from math import abs

# Create your views here.
def dashboard(request, user=None, *args, **kwargs):
    Objects = User.objects.all()
    cont = {
        'username' : None,
        'user' : None,
    }
    check = 0
    if request.method == 'POST' and user == None:
        username =  request.POST['username']
        password =  request.POST['password']
        for user in Objects:
            if username == user.username and password == user.password:
                check = '1'
                break
    if check == '1':
        calcul_expense(username)
        calcul_income(username)
        calcul_balance(username)
        get_piechart(username)
        return userFound(request, username)
    else:
        return redirect('/?check=0')


def userFound(request, user=None):
    obj = User.objects.get(username=user)
    trans = []
    data = Transaction.objects.all()
    for x in data:
        if x.username == user and x.Type == 'Expense':
            trans.append(x)
    context = {
        'username' : user,
        'user'  : obj,
        'data' : trans,
        'growth': calcul_growth(user),
    }
    context['graph'] = get_piechart(user)
    return render(request, 'dashboard/dashboard.html', context=context)

def add_trans(request, user=None):
    if request.method == 'POST':
        title = request.POST['title']
        date = request.POST['date']
        Type = request.POST['type']
        amount = request.POST['amount']
        Category = request.POST['category']
        user = request.POST['user']
        obj = Transaction(title=title,date=date, Type=Type, amount=amount, Category=Category, username=user)
        obj.save()
    obj = User.objects.get(username=user)
    trans = []
    data = Transaction.objects.all()
    for x in data:
        if x.username == user and x.Type == 'Expense':
            trans.append(x)
    cont = {
        'username': user,
        'user' : obj,
        'data' : trans,
        'growth': calcul_growth(user),
    }
    cont['graph'] = get_piechart(user)
    calcul_expense(user)
    calcul_income(user)
    calcul_balance(user)
    return render(request, 'dashboard/dashboard.html', cont)

def del_trans(request, user=None):
    user = request.GET['user']
    Id = request.GET['id']
    Transaction.objects.filter(Id=Id).delete()
    obj = User.objects.get(username=user)
    trans = []
    data = Transaction.objects.all()
    for x in data:
        if x.username == user and x.Type == 'Expense':
            trans.append(x)
    cont = {
        'username': user,
        'user' : obj,
        'data' : trans,
        'growth': calcul_growth(user),
    }
    cont['graph'] = get_piechart(user)
    calcul_expense(user)
    calcul_income(user)
    calcul_balance(user)
    return render(request, 'dashboard/dashboard.html', cont)

def calcul_expense(user):
    userExp = 1
    obj = User.objects.get(username=user)
    exp = Transaction.objects.all()
    for x in exp:
        if x.username == user and x.Type == 'Expense':
            userExp += x.amount
    User.objects.filter(username=user).update(expense=userExp)
    return userExp

def calcul_income(user):
    userInco = 1
    obj = User.objects.get(username=user)
    exp = Transaction.objects.all()
    for x in exp:
        if x.username == user and x.Type == 'Income':
            userInco += x.amount
    User.objects.filter(username=user).update(income=userInco)
    return userInco

def calcul_balance(user):
    balance = calcul_income(user) - calcul_expense(user)
    obj = User.objects.get(username=user)
    User.objects.filter(username=user).update(balance=balance)
    return balance

def calcul_growth(user):
    balance = calcul_balance(user)
    origin = calcul_income(user)
    growth = ((balance - origin) / abs(origin)) * 100
    return "{:.2f}".format(growth)

def get_piechart(user):
    data = {
        'Housing': 0,
        'School': 0,
        'Transportation': 0,
        'Insurance': 0,
        'Medical' : 0,
        'Saving': 0,
        'Shooping': 0,
    }
    Objs = Transaction.objects.all()
    for x in Objs:
        if x.username == user and x.Type == 'Expense':
            data[x.Category] += x.amount
    cat = []
    values = []
    for x in data:
        if data[x] != 0:
            cat.append(x)
            values.append(data[x])
            
    #making the pie chart
    myexplode = [0.2] + [0 for x in cat]
    myexplode.pop(-1)
    print(myexplode)
    fig = plt.figure()
    plt.pie(values, labels=cat, explode=myexplode, shadow=True, autopct='%1.1f%%')

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    img = imgdata.getvalue()
    return img