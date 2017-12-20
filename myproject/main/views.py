# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request, 'index_main.html')

@csrf_exempt
def runscript(request):
    if request.method == 'POST':
        return "SSSS"
