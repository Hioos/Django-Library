import datetime
import random
import string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q, Prefetch
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
# Create your views here.
from django.template import loader
from django.urls import reverse

from .models import Account
from django.conf import settings


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
            messages.success(request, 'Hello ' + request.session['name'] + ', Welcome Back !!!')
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
@login_required
def userIndex(request):
    accounts = Account.objects.filter(is_admin = False, is_staff= False, is_superuser=False)
    template = loader.get_template('users/index.html')
    def accountCounter():
        count = Account.objects.filter(is_admin = False, is_staff= False, is_superuser=False).count()
        return count
    currentlyOnline = Account.objects.filter(is_active=True).count()
    x = accountCounter()
    context = {
        'accounts' : accounts,
        'currentlyOnline': currentlyOnline,
        'x': x,
    }
    # str(authors.query)
    return HttpResponse(template.render(context, request))
@login_required
def add(request):
    template = loader.get_template('users/add.html')
    return HttpResponse(template.render({},request))
@login_required
def addUser(request):
    def randomUsername():
        source = string.ascii_letters + string.digits
        result_str = 'HL'+''.join((random.choice(source) for i in range(8)))
        return result_str
    def randomPassword():
        source = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(source) for i in range(12)))
        return result_str
    email = request.POST['email']
    username = randomUsername()
    password = randomPassword()
    name = request.POST['name']
    phone_number = request.POST['phone_number']
    address = request.POST['address']
    birth_date = request.POST['birth_date']
    expired_date = request.POST['expired_date']
    national_id = request.POST['national_id']
    date_joined = datetime.datetime.now
    created_by = Account.objects.get(id=request.session['id'])
    Account.objects.create_user(email=email,
                                username=username,
                                password=password,
                                name=name,
                                 date_joined=date_joined,
                                 phone_number=phone_number,
                                 address=address,
                                 birth_date=birth_date,
                                 expired_date=expired_date,
                                 national_id=national_id,
                                 created_by=created_by.id)
    subject = 'Welcome to HiusLibrary'
    message = f'Hi {name}, thank you for registering in HiusLibrary. \n' \
                    f'This is your Access Key and Password for www.hiuslibrary.vn \n' \
                    f'Please do not share this information with anyone. \n' \
                    f'Access Key: {username} \n' \
                    f'Password: {password} \n' \
                    f'\t\t\t Sincerely, \n' \
                    f'\t\t\t {created_by.name}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
    messages.success(request, "The user is successfully registered !!!")
    return HttpResponseRedirect(reverse('userIndex'))
@login_required
def adminIndex(request):
    accounts = Account.objects.filter(is_staff = True)
    template = loader.get_template('administrator/index.html')
    def accountCounter():
        count = Account.objects.filter(is_staff = True).count()
        return count
    x = accountCounter()
    context = {
        'accounts' : accounts,
        'x': x,
    }
    # str(authors.query)
    return HttpResponse(template.render(context, request))
@login_required
def updateProfile(request):
    user = Account.objects.get(id=request.session['id'])
    template = loader.get_template('administrator/update_profile.html')
    context = {
        'user' : user
    }
    # str(authors.query)
    return HttpResponse(template.render(context, request))
@login_required
def info(request,id):
    user = Account.objects.filter(Q(is_staff= True) | Q(is_admin = True ) | Q(is_superuser = True)).get(id=id)
    template = loader.get_template('administrator/info.html')
    createdBy = Account.objects.filter(created_by = id).prefetch_related(Prefetch('user_created_by', Account.objects.filter(created_by=id))).order_by('date_joined')[:5][::-1]
    counter = Account.objects.filter(created_by=id).prefetch_related(
        Prefetch('user_created_by', Account.objects.filter(created_by=id))).count()
    a =request.session['id']
    context = {
            'user' : user,
            'a' : a,
            'counter': counter,
            'createdBy': createdBy
    }
    return HttpResponse(template.render(context, request))
@login_required
def extendMembership(request,id):
    user = Account.objects.get(id = id)
    user.expired_date = user.expired_date + datetime.timedelta ( seconds=1*31*24*60*60 )
    user.save()
    return HttpResponseRedirect(reverse('userIndex'))
@login_required
def banUser(request):
    data = request.GET['catid']
    admin = Account.objects.get(id=request.session['id'])
    user =Account.objects.get(id = data)
    if user.is_banned is True:
        user.is_banned = False
    elif user.is_banned is False:
        user.is_banned = True
        user.expired_date= datetime.datetime.today()
        user.banned_by = admin
    user.save()
    return HttpResponseRedirect(reverse('userIndex'))

