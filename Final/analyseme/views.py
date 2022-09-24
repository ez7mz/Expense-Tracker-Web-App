from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import AnlyseFile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

FILE_EXT = ['csv', 'xlsx', 'xls']
USE_COLS = ['Date', 'Category', 'Type', 'Amount']

def home(request):
    cont = {
        'check' : 0,
        'list' : [-1, 0, 2, 3],
    }
    return render(request, 'analyseMe/analyseMe.html', cont)

# Create your views here.
def analyseMe(request):
    cont = test(request)
    return render(request, 'analyseMe/analyseMe.html', cont)

def test(request):
    cont = {
        'check' : 0,
        'list' : [-1, 0, 2, 3],
    }
    if request.method == 'POST':
        file_name = str(request.FILES['data'])
        file_ext = str(file_name).split(".")[-1].lower()
        file = request.FILES.get(u'data')
        if file_ext in FILE_EXT:
            try:
                # CLEANING THE DATA
                df = pd.read_csv(file, usecols=USE_COLS)
                df = cleaning_the_data(df)
                print(df.head())

                # GET EXPENSE DATA
                exp_tot, exp_data = get_exp_data(df)
                exp_labels = list(exp_data.keys())
                exp_val = list(exp_data.values())
                
                # GET INCOME DATA
                inc_tot, inc_data = get_inc_data(df)
                inc_labels = list(inc_data.keys())
                inc_val = list(inc_data.values())

                # GET EXPENSE AND INCOME CHARTS
                if len(exp_labels) != 0 and len(exp_val) != 0:
                    exp_pie = piecahrt_maker(exp_labels, exp_val)
                    exp_bar = barchart_maker(exp_labels, exp_val)

                # if len(inc_labels) != 0 and len(inc_val) != 0:
                #     inc_pie = piecahrt_maker(inc_labels, inc_val)
                #     inc_bar = barchart_maker(inc_labels, inc_val)

                # CALCULATE AVRG AND MODE
                avrg = sum(exp_val) / len(exp_val)
                mode = list(dict(sorted(exp_data.items(), key=lambda item: item[1])).keys())[-1]
                
                # MAKE CONTEXT TO SEND TO TEMPLATES
                cont['check'] = 1
                cont['exp_tot'] = "{:.2f}".format(exp_tot)
                cont['inc_tot'] = "{:.2f}".format(inc_tot)
                cont['avrg'] = "{:.2f}".format(avrg)
                cont['mode'] = mode
                cont['exp_pie'] = exp_pie
                cont['exp_bar'] = exp_bar
                # cont['inc_pie'] = inc_pie
                # cont['inc_bar'] = inc_bar
            except:
                cont['check'] = -1
        else :
            cont['check'] = 2
    else:
        cont['check'] = 3
    return cont

def cleaning_the_data(df):
    df['Amount'] = df['Amount'].fillna(0)
    df['Category'] = df['Category'].fillna('Other')
    df=df.dropna()
    return df

def get_exp_data(df):
    # working with expenses
    head = []
    exp_data = {}
    i = 0
    TOT_EXP = 0.0
    for x in df:
        head.append(x)
    # print(head)

    for x in df.values:
        if x[head.index('Type')].lower() == 'expense':
            exp_data[x[head.index('Category')]] = 0
    # print(list(exp_data.keys()))
    for x in df.values:
        y = x[head.index('Category')]
        if x[head.index('Type')].lower() == 'expense':
            TOT_EXP += x[head.index('Amount')]
            exp_data[y] += x[head.index('Amount')]
    # print(exp_data)
    # print(TOT_EXP)
    return TOT_EXP, exp_data

def get_inc_data(df):
    # working with incomes
    head = []
    inc_data = {}
    i = 0
    TOT_INC = 0.0
    for x in df:
        head.append(x)
    print(head)

    for x in df.values:
        if x[head.index('Type')].lower() == 'income':
            inc_data[x[head.index('Category')]] = 0
    print(list(inc_data.keys()))
    for x in df.values:
        y = x[head.index('Category')]
        if x[head.index('Type')].lower() == 'income':
            TOT_INC += x[head.index('Amount')]
            inc_data[y] += x[head.index('Amount')]
    print(inc_data)
    print(TOT_INC)
    return TOT_INC, inc_data

def piecahrt_maker(labels, val):
    fig = plt.figure()
    marg = 0.364
    if len(labels) > 13:
        marg = 0.450
    fig.subplots_adjust(left=marg, bottom=0.10, right=0.99, top=0.97)
    porcent = []
    for x in val:
        porcent.append((x * 100)/sum(val))
    patches, texts = plt.pie(val, startangle=90, radius=1.2)
    y = []
    y = [f"{i} - {j:.2f}%" for i,j in zip(labels, porcent)]
    # labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels, porcent)]

    sort_legend = True
    if sort_legend:
        patches, labels, dummy =  zip(*sorted(zip(patches, labels, val),
                                            key=lambda x: x[2],
                                            reverse=True))

    plt.legend(patches, y, loc='best', bbox_to_anchor=(-0.1, 1.),
            fontsize=8)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    img = imgdata.getvalue()
    return img

def barchart_maker(labels, val):
    fig = plt.figure()
    fig.clf()
    ax = fig.add_subplot(111)

    ax.yaxis.grid(True, linestyle='-', which='major', color='grey', alpha=0.5)

    rects = ax.bar(labels, val, width=0.2, align='center', color='thistle')
    ax.set_xticks(labels)
    #function to auto-rotate the x axis labels
    fig.autofmt_xdate()

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    img = imgdata.getvalue()
    return img