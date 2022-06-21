from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import datetime
from django.urls import reverse

from .models import Users
import random
import string
import secrets  # import package
from django.conf import settings
from django.core.mail import send_mail
from ..administrator.models import Administrator


def random():
    num = 10  # define the length of the string
    # define the secrets.choice() method and pass the string.ascii_letters + string.digits as an parameters.
    res = 'HL'+''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num))

    # print the Secure string
    return str(res)
def index(request):
    users = Users.objects.all()
    count = Users.objects.count()
    template = loader.get_template('users/index.html')
    context = {
            'users': users,
            'count' : count
    }
    return HttpResponse(template.render(context, request))
def add(request):
    template = loader.get_template('users/add.html')
    return HttpResponse(template.render({},request))
def addNewMember(request):
    userName = request.POST['userName']
    userEmail = request.POST['userEmail']
    userAddress = request.POST['userAddress']
    userNationalId = request.POST['userNationalId']
    userDoB = request.POST['userDoB']
    userEnd = request.POST['userEnd']
    userPhone = request.POST['userPhone']
    userUserName = random()
    userPassword = random()
    userCreatedAt = datetime.datetime.now()
    userCreatedBy = Administrator.objects.get(id=1)
    userStart = datetime.datetime.today().date()
    userPermission = True
    subject = 'Welcome to HiusLibrary'
    html_message = f'Hi {userName}, thank you for registering in HiusLibrary. \n' \
              f'This is your Access Key and Password for www.hiuslibrary.vn \n' \
              f'Please do not share this information with anyone. \n' \
              f'Access Key: {userUserName}\n' \
              f'Password: {userPassword} \n' \
              f'\t\t                                                Sincerely,\n' \
              f'\t\t                                                     Hius'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [userEmail]
    send_mail(subject, html_message, email_from, recipient_list)
    user = Users(user_name = userName,
                 user_address = userAddress,
                 user_email = userEmail,
                 user_phoneNumber = userPhone,
                 user_nationalIdentificationNumber = userNationalId,
                 user_dateOfBirth = userDoB,
                 user_userName = userUserName,
                 user_password = userPassword,
                 user_permission = userPermission,
                 user_createdAt = userCreatedAt,
                 user_updatedAt = userCreatedAt,
                 user_membershipStart = userStart,
                 user_membershipEnd = userEnd,
                 user_createdBy = userCreatedBy,
                 user_updatedBy = userCreatedBy)
    user.save()
    return HttpResponseRedirect(reverse('userIndex'))
def extend(request,id):
    userUpdatedAt = datetime.datetime.now()
    future = userUpdatedAt + datetime.timedelta ( seconds=1*30*24*60*60)
    user = Users.objects.get(user_id=id)
    user.user_membershipEnd = future
    user.user_updatedAt = userUpdatedAt
    user.save()
    return HttpResponseRedirect(reverse('userIndex'))
def block(request,id):
    userUpdatedAt = datetime.datetime.now()
    user = Users.objects.get(user_id=id)
    if user.user_permission:
        x = False
    else:
        x = True
    user.user_permission = x
    user.user_updatedAt = userUpdatedAt
    user.save()
    return HttpResponseRedirect(reverse('userIndex'))