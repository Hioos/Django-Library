import datetime
from venv import create

from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.urls import reverse

from .models import loanStatus
from django.contrib.auth.decorators import login_required

from ..accounts.models import Account

def LogEntryAdd(idUser,modelName,objectId,reason,after):
    LogEntry.objects.log_action(
        user_id=idUser,
        content_type_id=ContentType.objects.get_for_model(modelName).pk,
        object_id=objectId,
        object_repr=reason,
        change_message=after,
        action_flag=ADDITION if create else CHANGE)

@login_required
def index(request):
    loans = loanStatus.objects.all()
    template = loader.get_template('loan/index.html')
    context = {
            'loans': loans,
    }
    return HttpResponse(template.render(context, request))

def add(request):
    statusName = request.POST['statusName']
    loan = loanStatus(loanStatus_name = statusName)
    loan.save()
    LogEntryAdd(request.session['id'], loan, '', '', statusName)
    messages.success(request,statusName + ' added successfully !!!')
    return HttpResponseRedirect(reverse('loanIndex'))