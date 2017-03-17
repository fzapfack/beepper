from django.shortcuts import render
from django.http import HttpResponse
from .utils import doctoctoc


# Create your views here.
def load_data(request):
    print('Loading data from xls')

    return HttpResponse('Twitter listener started')
