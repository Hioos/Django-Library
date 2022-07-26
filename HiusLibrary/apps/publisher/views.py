import datetime
from venv import create
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.template import loader
from django.urls import reverse

from .models import Publisher
from django.contrib.auth.decorators import login_required
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from ..accounts.models import Account
from ..book import models
from ..book.models import Books


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
    publishers = Publisher.objects.annotate(num_assets=Count('book_publisher'))
    x = Publisher.objects.count()
    template = loader.get_template('publisher/index.html')
    context = {
        'x': x,
        'publishers': publishers,
    }
    return HttpResponse(template.render(context, request))


@login_required
def add(request):
    ctype = ContentType.objects.get(model='publisher')
    publisherName = request.POST['publisherName']
    publisher = Publisher(publisher_name=publisherName)
    publisher.save()
    LogEntryAdd(request.session['id'], publisher,'', 'Add',publisherName)
    messages.success(request, ' Added successfully !!!')
    return HttpResponseRedirect(reverse('publisherIndex'))
