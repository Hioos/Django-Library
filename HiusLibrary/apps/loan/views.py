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

from ..accounts.models import Account, Pricing


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
@login_required
def add(request):
    statusName = request.POST['statusName']
    loan = loanStatus(loanStatus_name = statusName)
    loan.save()
    LogEntryAdd(request.session['id'], loan, '', '', statusName)
    messages.success(request,statusName + ' added successfully !!!')
    return HttpResponseRedirect(reverse('loanIndex'))
@login_required
def pricing(request):
    pricing = Pricing.objects.all().order_by('pricing_price')
    template = loader.get_template('loan/pricing.html')
    context = {
        'pricing':pricing,
    }
    return HttpResponse(template.render(context,request))
@login_required
def addpricing(request):
    pricing_name = request.POST['pricing_name']
    price = request.POST['price']
    price_image = request.FILES.get('price_image')
    days = request.POST['days']
    pricing = Pricing(
        pricing_name = pricing_name,
        pricing_price = price,
        pricing_days = days,
        pricing_image =price_image
    )
    pricing.save()
    messages.success(request, pricing_name + ' added successfully !!!')
    return HttpResponseRedirect(reverse('pricing'))
@login_required
def loanEdit(request,id):
    loan_name = request.POST['statusName_update']
    loan = loanStatus.objects.get(loanStatus_id=id)
    loan.loanStatus_name = loan_name
    loan.save()
    messages.success(request, loan_name + ' updated successfully !!!')
    return HttpResponseRedirect(reverse('loanIndex'))
@login_required
def pricingEdit(request,id):
    pricing_name = request.POST['pricingName_update']
    pricing_price = request.POST['pricingPrice_update']
    price_image = request.FILES.get('price_image_update')
    price_day = request.POST['pricingDay_update']
    price = Pricing.objects.get(pricing_id=id)
    if price_image is None:
        price.pricing_name = pricing_name
        price.pricing_price = pricing_price
        price.pricing_days = price_day
    else:
        price.pricing_name = pricing_name
        price.pricing_price = pricing_price
        price.pricing_image = price_image
        price.pricing_days = price_day
    price.save()
    messages.success(request, pricing_name + ' updated successfully !!!')
    return HttpResponseRedirect(reverse('pricing'))
@login_required
def editPricing(request,id):
    pricing = Pricing.objects.get(pricing_id=id)
    template = loader.get_template('loan/edit.html')
    context = {
        'price':pricing,
    }
    return HttpResponse(template.render(context,request))
