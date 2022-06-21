from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import datetime
# Create your views here.
from django.template import loader
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Administrator


def index(request):
    administratorMembers = Administrator.objects.all().values()
    template = loader.get_template('administrator/index.html')
    context = {
            'administratorMembers': administratorMembers,
    }
    return HttpResponse(template.render(context, request))
def add(request):
    template = loader.get_template('administrator/add.html')
    return HttpResponse(template.render({},request))
def addNewAdministrator(request):
    adminName = request.POST['adminName']
    adminUserName = request.POST['adminUserName']
    adminEmail = request.POST['adminEmail']
    adminDoB = request.POST['adminDoB']
    adminPassword = request.POST['adminPassword']
    adminConfirmPassword = request.POST['adminConfirmPassword']
    adminNationalId = request.POST['adminNationalId']
    adminRole = request.POST['adminRole']
    adminUpdatedAt = datetime.datetime.now()
    adminStatus = False
    adminCreatedAt = datetime.datetime.now()
    adminLastLogin = datetime.datetime.now()
    admin = Administrator(administrator_name=adminName,
                                  administrator_username=adminUserName,
                                  administrator_password=adminPassword,
                                  administrator_email=adminEmail,
                                  administrator_dateOfBirth=adminDoB,
                                  administrator_nationalIdentificationNumber=adminNationalId,
                                  administrator_role=adminRole,
                                  administrator_updatedAt=adminUpdatedAt,
                                  administrator_status=adminStatus,
                                  administrator_createdAt=adminCreatedAt,
                                  administrator_lastLogin=adminLastLogin)
    admin.save()
    return HttpResponseRedirect(reverse('adminIndex'))
def changeRole(request,id):
    administrator = Administrator.objects.get(id=id)
    adminUpdatedAt = datetime.datetime.now()
    if administrator.administrator_role == 1:
        administrator.administrator_role = 0
    elif administrator.administrator_role == 0:
        administrator.administrator_role = 1
    administrator.administrator_updatedAt = adminUpdatedAt
    administrator.save()
    return HttpResponseRedirect(reverse('adminIndex'))