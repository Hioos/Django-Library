import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.urls import reverse

from .models import Authors
from ..administrator.models import Administrator
def authorCounter():
    count = Authors.objects.all().count()
    return count
def index(request):
    authors = Authors.objects.select_related()
    template = loader.get_template('authors/index.html')
    x = authorCounter()
    context = {
        'authors' : authors,
        'x': x,
    }
    # str(authors.query)
    return HttpResponse(template.render(context, request))
def add(request):
    template = loader.get_template('authors/add.html')
    return HttpResponse(template.render({},request))
def addNewAuthor(request):
    authorName = request.POST['authorName']
    authorDoB = request.POST['authorDoB']
    authorBio = request.POST['authorBio']
    authorImgUrl = request.POST['imgUrl']
    authorNationalityURL = request.POST['nationUrl']
    authorGender = request.POST['authorGender']
    authorCreatedAt = datetime.datetime.now()
    authorUpdatedAt = datetime.datetime.now()
    author = Authors(author_name = authorName,
                     author_dateOfBirth = authorDoB,
                     author_biography = authorBio,
                     author_imgUrl = authorImgUrl,
                     author_nationalImgUrl = authorNationalityURL,
                     author_createdAt = authorCreatedAt,
                     author_updatedAt = authorUpdatedAt,
                     author_gender = authorGender)
    author.save()
    return HttpResponseRedirect(reverse('authorsIndex'))
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
def updateProcess(request,id):
    authorName = request.POST['authorName']
    authorDoB = request.POST['authorDoB']
    imgUrl = request.POST['imgUrl']
    nationUrl = request.POST['nationUrl']
    authorBio = request.POST['authorBio']
    authorGender = request.POST['authorGender']
    authorUpdatedAt = datetime.datetime.now()
    author = Authors.objects.get(author_id = id)
    author.author_name = authorName
    author.author_dateOfBirth = authorDoB
    author.author_biography = authorBio
    author.author_imgUrl = imgUrl
    author.author_nationalImgUrl = nationUrl
    author.author_gender = authorGender
    author.author_updatedAt = authorUpdatedAt
    author.save()
    return HttpResponseRedirect(reverse('authorsIndex'))