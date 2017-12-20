# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request, 'index_main.html')

def runscript(request):
    email = request.GET['email']
    username = request.GET['username']
    host = request.GET['host']
    domain = request.GET['domain']
    password = request.GET['password']
    return render(request, 'run_script.html',{"email" : email, "username" : username, "host" : host,"domain" : domain , "password" : password})
