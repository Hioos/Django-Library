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

from django.contrib.auth.decorators import login_required

from .models import Authors
from ..accounts.models import Account
from ..book.models import BookAuthorship


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
    authors = Authors.objects.select_related().order_by('-author_id')
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
    messages.success(request, (authorName + ' Added Successfully !!!'))
    return HttpResponseRedirect(reverse('authorsIndex'))
@login_required
def update(request,id):
    author = Authors.objects.get(author_id = id)
    template = loader.get_template('authors/update.html')
    context = {
        'author': author
    }
    return HttpResponse(template.render(context,request))
@login_required
def updateProcess(request,id):
    authorName = request.POST['authorName']
    reason = request.POST['reason']
    authorDoB = request.POST['authorDoB']
    authorPseudonym = request.POST['authorPseudonym']
    imgUrl = request.FILES.get('image')
    authorBio = request.POST['authorBio']
    authorGender = request.POST['authorGender']
    author = Authors.objects.get(author_id = id)
    if imgUrl is None:
        author.author_name = authorName
        author.author_dateOfBirth = authorDoB
        author.author_biography = authorBio
        author.author_pseudonym = authorPseudonym
        author.author_gender = authorGender
    else:
        author.author_name = authorName
        author.author_dateOfBirth = authorDoB
        author.author_biography = authorBio
        author.author_imgUrl = imgUrl
        author.author_pseudonym = authorPseudonym
        author.author_gender = authorGender
    author.save()
    LogEntryAdd(request.session['id'], author,'',reason, authorName)
    messages.success(request, (authorName + ' Updated Successfully !!!'))
    return HttpResponseRedirect(reverse('authorsIndex'))
@login_required
def byAuthor(request,id):
    books = BookAuthorship.objects.filter(bookauthorship_authorId=id).prefetch_related()
    template = loader.get_template('authors/books.html')
    context = {
        'books' : books
    }
    return HttpResponse(template.render(context,request))