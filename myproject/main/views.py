# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index_main.html')

def runscript(request):
    if request.method == 'POST':
        email = request.POST.get('email','')
        username = request.POST.get('username','')
        host = request.POST.get('host','')
        domain = request.POST.get('domain','')
        password = request.POST.get('password','')
        return render(request, 'run_script.html',{"email" : email, "username" : username, "host" : host,"domain" : domain , "password" : password})
