import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.urls import reverse

from .models import loanStatus
from ..administrator.models import Administrator


def index(request):
    loans = loanStatus.objects.all()
    template = loader.get_template('loan/index.html')
    context = {
            'loans': loans,
    }
    return HttpResponse(template.render(context, request))

def add(request):
    statusName = request.POST['statusName']
    loanCreatedAt = datetime.datetime.now()
    intModifiedUser = Administrator.objects.get(id=1)

    loan = loanStatus(loanStatus_name = statusName,
                      loanStatus_createdAt = loanCreatedAt,
                      loanStatus_updatedAt = loanCreatedAt,
                      loanStatus_createdBy = intModifiedUser,
                      loanStatus_updatedBy = intModifiedUser,)
    loan.save()
    return HttpResponseRedirect(reverse('loanIndex'))