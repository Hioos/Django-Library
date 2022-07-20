from venv import create

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import datetime

from django.urls import reverse

from .models import Genre, SubGenre, Themes
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
    genres = Genre.objects.all()
    count = Genre.objects.count()
    template = loader.get_template('genre/index.html')
    context = {
            'genres': genres,
            'count': count,
    }

    return HttpResponse(template.render(context, request))
@login_required
def add(request):
    template = loader.get_template('genre/add.html')
    return HttpResponse(template.render({},request))
@login_required
def addNewGenre(request):
    genreName = request.POST['genreName']
    genreCode = request.POST['genreCode']
    genreDesc = request.POST['genreDesc']
    genre = Genre(genre_name = genreName,
                  genre_description = genreDesc,
                  genre_code = genreCode,
                  )
    genre.save()
    LogEntryAdd(request.session['id'], genre, '', '', genreName)
    return HttpResponseRedirect(reverse('genreIndex'))
@login_required
def update(request, id):
    genre = Genre.objects.get(id = id)
    template = loader.get_template('genre/update.html')
    context = {
        'genre' : genre,
    }
    return HttpResponse(template.render(context,request))
@login_required
def updateGenreProcess(request,id):
    genreName = request.POST['genreName']
    reason = request.POST['reason']
    genreCode = request.POST['genreCode']
    genreDesc = request.POST['genreDesc']
    admin = Account.objects.get(id=request.session['id'])
    genre = Genre.objects.get(id=id)
    genre.genre_name = genreName
    genre.genre_code = genreCode
    genre.genre_description = genreDesc
    genre.save()
    LogEntryAdd(request.session['id'], genre, '', reason, genreName)
    return HttpResponseRedirect(reverse('genreIndex'))
@login_required
def subGenre(request,id):
    subGenre = SubGenre.objects.filter(subgenre_ofGenre=id).prefetch_related('subgenre_ofGenre')
    genre = Genre.objects.get(id=id)
    subGenreCount = SubGenre.objects.filter(subgenre_ofGenre=id).count()
    template = loader.get_template('genre/subgenre.html')
    context = {
            'genre' : genre,
            'subGenre': subGenre,
            'subGenreCount': subGenreCount,
    }
    return HttpResponse(template.render(context, request))
@login_required
def subGenreAdd(request,id):
    template = loader.get_template('genre/subGenreAdd.html')
    genre = Genre.objects.get(id=id)
    context = {
        'genre': genre
    }
    return HttpResponse(template.render(context,request))
@login_required
def addNewSubGenre(request,id):
    subGenreName = request.POST['subGenreName']
    subGenreCode = request.POST['subGenreCode']
    subGenreDesc = request.POST['subGenreDesc']
    subGenre = SubGenre(
                  subgenre_name = subGenreName,
                  subgenre_description = subGenreDesc,
                  subgenre_code = subGenreCode,
                    subgenre_ofGenre=Genre.objects.get(id=id),
                )
    subGenre.save()
    LogEntryAdd(request.session['id'], subGenre, '', '', subGenreName)
    return HttpResponseRedirect(reverse('subgenre',args=[id]))
@login_required
def subGenreUpdate(request,id):
    subGenre = SubGenre.objects.get(id = id)
    template = loader.get_template('genre/subGenreUpdate.html')
    context = {
        'subGenre' : subGenre,
    }
    return HttpResponse(template.render(context,request))
@login_required
def updateSubGenreProcess(request,id):
    subGenreName = request.POST['subGenreName']
    subGenreCode = request.POST['subGenreCode']
    subGenreDesc = request.POST['subGenreDesc']
    reason = request.POST['reason']
    field_name = 'subgenre_ofGenre'
    obj = SubGenre.objects.first()
    field_object = SubGenre._meta.get_field(field_name)
    field_value = field_object.value_from_object(obj)
    subGenre = SubGenre.objects.get(id=id)
    subGenre.subgenre_name = subGenreName
    subGenre.subgenre_code = subGenreCode
    subGenre.subgenre_description = subGenreDesc
    subGenre.save()
    LogEntryAdd(request.session['id'], subGenre, '', reason, subGenreName)
    return HttpResponseRedirect(reverse('subgenre',args=[field_value]))
@login_required
def themes(request):
    themes = Themes.objects.all()
    count = Themes.objects.count()
    template = loader.get_template('genre/themes.html')
    context = {
            'themes': themes,
            'count': count,
    }
    return HttpResponse(template.render(context, request))
@login_required
def themeAdd(request):
    template = loader.get_template('genre/themesAdd.html')
    return HttpResponse(template.render({},request))
@login_required
def addNewTheme(request):
    themeName = request.POST['themeName']
    themeDesc = request.POST['themeDesc']
    theme = Themes(
        theme_name = themeName,
        theme_description = themeDesc,
    )
    theme.save()
    LogEntryAdd(request.session['id'], theme, '', '', themeName)
    return HttpResponseRedirect(reverse('themes'))
@login_required
def editTheme(request,id):
    theme = Themes.objects.get(theme_id=id)
    template = loader.get_template('genre/editTheme.html')
    context = {
        'theme' : theme
    }
    return HttpResponse(template.render(context,request))
@login_required
def updateTheme(request,id):
    themeName = request.POST['themeName']
    themeDesc = request.POST['themeDesc']
    reason = request.POST['reason']
    theme = Themes.objects.get(theme_id = id)
    theme.theme_name = themeName
    theme.theme_description = themeDesc
    theme.save()
    LogEntryAdd(request.session['id'], theme, '', reason, themeName)
    return HttpResponseRedirect(reverse('themes'))
