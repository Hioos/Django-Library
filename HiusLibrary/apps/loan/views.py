import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.urls import reverse

from .models import loanStatus
from django.contrib.auth.decorators import login_required

from ..accounts.models import Account


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
    loanCreatedAt = datetime.datetime.now()
    admin = Account.objects.get(id=request.session['id'])
    loan = loanStatus(loanStatus_name = statusName,
                      loanStatus_createdAt = loanCreatedAt,
                      loanStatus_updatedAt = loanCreatedAt,
                      loanStatus_createdBy = admin,
                      loanStatus_updatedBy = admin)
    loan.save()
    return HttpResponseRedirect(reverse('loanIndex'))