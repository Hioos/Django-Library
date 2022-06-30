import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.urls import reverse

from .models import Publisher
from django.contrib.auth.decorators import login_required

from ..accounts.models import Account


@login_required
def index(request):
    publishers = Publisher.objects.all()
    x = Publisher.objects.count()
    template = loader.get_template('publisher/index.html')
    context = {
            'x' : x,
            'publishers': publishers,
    }
    return HttpResponse(template.render(context, request))

def add(request):
    publisherName = request.POST['publisherName']
    publisherCreatedAt = datetime.datetime.now()
    admin = Account.objects.get(id=request.session['id'])
    publisher = Publisher(publisher_name = publisherName,
                      publisher_createdAt = publisherCreatedAt,
                      publisher_updatedAt = publisherCreatedAt,
                      publisher_createdBy = admin,
                      publisher_updatedBy = admin)
    publisher.save()
    messages.success(request,publisherName + ' added successfully !!!')
    return HttpResponseRedirect(reverse('publisherIndex'))