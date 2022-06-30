from django.db.models import Count, Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import datetime

from django.urls import reverse

from .models import Genre, SubGenre, Themes
from django.contrib.auth.decorators import login_required

from ..accounts.models import Account


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
    genreUpdatedAt = datetime.datetime.now()
    genreCreatedAt = datetime.datetime.now()
    admin = Account.objects.get(id=request.session['id'])
    genre = Genre(genre_name = genreName,
                  genre_description = genreDesc,
                  genre_code = genreCode,
                  genre_updatedAt = genreUpdatedAt,
                  genre_createdAt = genreCreatedAt,
                  genre_createdBy = admin,
                  genre_updatedBy = admin
                  )
    genre.save()
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
    genreCode = request.POST['genreCode']
    genreDesc = request.POST['genreDesc']
    genreUpdatedAt = datetime.datetime.now()
    admin = Account.objects.get(id=request.session['id'])
    genre = Genre.objects.get(id=id)
    genre.genre_name = genreName
    genre.genre_code = genreCode
    genre.genre_description = genreDesc
    genre.genre_updatedAt = genreUpdatedAt
    genre.genre_updatedBy = admin
    genre.save()
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
    subGenreUpdatedAt = datetime.datetime.now()
    subGenreCreatedAt = datetime.datetime.now()
    admin = Account.objects.get(id=request.session['id'])
    subGenre = SubGenre(
                  subgenre_name = subGenreName,
                  subgenre_description = subGenreDesc,
                  subgenre_code = subGenreCode,
                  subgenre_updatedAt = subGenreUpdatedAt,
                  subgenre_createdAt = subGenreCreatedAt,
                  subgenre_ofGenre = Genre.objects.get(id=id),
                    subgenre_createdBy = admin,
                    subgenre_updatedBy = admin
                )

    subGenre.save()
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
    field_name = 'subgenre_ofGenre'
    obj = SubGenre.objects.first()
    field_object = SubGenre._meta.get_field(field_name)
    field_value = field_object.value_from_object(obj)
    admin = Account.objects.get(id=request.session['id'])
    subGenreUpdatedAt = datetime.datetime.now()
    subGenre = SubGenre.objects.get(id=id)
    subGenre.subgenre_name = subGenreName
    subGenre.subgenre_code = subGenreCode
    subGenre.subgenre_description = subGenreDesc
    subGenre.subgenre_updatedAt = subGenreUpdatedAt
    subGenre.subgenre_updatedBy = admin
    subGenre.save()
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
    timeCreated = datetime.datetime.now()
    admin = Account.objects.get(id=request.session['id'])
    theme = Themes(
        theme_name = themeName,
        theme_description = themeDesc,
        theme_createdAt = timeCreated,
        theme_updatedAt = timeCreated,
        theme_createdBy = admin,
        theme_updatedBy = admin
    )
    theme.save()
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
    themeUpdatedAt = datetime.datetime.now()
    admin = Account.objects.get(id=request.session['id'])
    theme = Themes.objects.get(theme_id = id)
    theme.theme_name = themeName
    theme.theme_description = themeDesc
    theme.theme_updatedAt = themeUpdatedAt
    theme.theme_updatedBy = admin
    theme.save()
    return HttpResponseRedirect(reverse('themes'))
