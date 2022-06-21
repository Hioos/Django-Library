from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader


def index(request):
    template = loader.get_template('misc/authentication/login.html')
    return HttpResponse(template.render({},request))
def login_user(request):
    if request.method == "POST":
        username = request.POST['adminUsername']
        password = request.POST['adminPassword']
        user = authenticate(request, administrator_username = username, administrator_password = password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.success(request,("Wrong password or Username"))
            return redirect('login')

    else:
        return render(request,'authentication')