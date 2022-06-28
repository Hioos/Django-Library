from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
# Create your views here.
from django.template import loader


def login_user(request):
    if request.method == "POST":
        username = request.POST['adminUsername']
        password = request.POST['adminPassword']
        user  =   authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            request.session['name'] = current_user.name
            request.session['id'] = current_user.id
            messages.success(request, request.session['name'])
            return  redirect('index')
        else:
            messages.success(request,('Wrong Username Or Password !!!'))
            return redirect('LogInAdmin')
    else:
        return render(request, 'misc/authentication/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request,("See You Soon !!"))
    return redirect('LogInAdmin')