import datetime
from venv import create
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import Authors
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
    authors = Authors.objects.select_related()
    template = loader.get_template('authors/index.html')
    def authorCounter():
        count = Authors.objects.all().count()
        return count
    x = authorCounter()
    context = {
        'authors' : authors,
        'x': x,
    }
    # str(authors.query)
    return HttpResponse(template.render(context, request))
@login_required
def add(request):
    template = loader.get_template('authors/add.html')
    return HttpResponse(template.render({},request))
@login_required
def addNewAuthor(request):
    authorName = request.POST['authorName']
    authorPseudonym = request.POST['authorPseudonym']
    authorDoB = request.POST['authorDoB']
    authorBio = request.POST['authorBio']
    authorImage = request.FILES.get('image')
    authorGender = request.POST['authorGender']
    author = Authors(author_name = authorName,
                     author_pseudonym = authorPseudonym,
                     author_dateOfBirth = authorDoB,
                     author_biography = authorBio,
                     author_imgUrl = authorImage,
                     author_gender = authorGender,)
    author.save()
    LogEntryAdd(request.session['id'], author,'','', authorName)
    return HttpResponseRedirect(reverse('authorsIndex'))
@login_required
def update(request,id):
    author = Authors.objects.get(author_id = id)
    authorGender = Authors.objects.values('author_gender').filter(author_id=id)
    if authorGender:
        x = 1
    else:
        x = 0
    template = loader.get_template('authors/update.html')
    context = {
        'author': author,
        'x' : x
    }
    return HttpResponse(template.render(context,request))
@login_required
def updateProcess(request,id):
    authorName = request.POST['authorName']
    reason = request.POST['reason']
    authorDoB = request.POST['authorDoB']
    imgUrl = request.POST['imgUrl']
    nationUrl = request.POST['nationUrl']
    authorBio = request.POST['authorBio']
    authorGender = request.POST['authorGender']
    author = Authors.objects.get(author_id = id)
    author.author_name = authorName
    author.author_dateOfBirth = authorDoB
    author.author_biography = authorBio
    author.author_imgUrl = imgUrl
    author.author_nationalImgUrl = nationUrl
    author.author_gender = authorGender
    author.save()
    LogEntryAdd(request.session['id'], author,'',reason, authorName)
    return HttpResponseRedirect(reverse('authorsIndex'))
