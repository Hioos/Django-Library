import datetime
from venv import create

from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Books, Language, BookAuthorship, BookSubGenre, BookThemes
# Create your views here.
from ..accounts.models import Account
from ..authors.models import Authors
from ..genre.models import SubGenre, Themes
from ..publisher.models import Publisher

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
    books = Books.objects.all().prefetch_related('book_Authorship_bookId','book_Subgenre_bookId','book_Themes_bookId')
    template = loader.get_template('books/index.html')
    def bookCounter():
        count = Books.objects.all().count()
        return count
    x = bookCounter()
    context = {
        'books' : books,
        'x': x,
    }
    return HttpResponse(template.render(context, request))
@login_required
def add(request):
    publishers = Publisher.objects.all().prefetch_related().select_related()
    languages = Language.objects.all()
    subgenres = SubGenre.objects.all().select_related('subgenre_ofGenre').order_by('subgenre_ofGenre_id')
    themes = Themes.objects.all()
    authors = Authors.objects.all()
    context={
        'publishers' : publishers,
        'languages' : languages,
        'subgenres' : subgenres,
        'themes'    : themes,
        'authors'   : authors
    }
    template = loader.get_template('books/add.html')
    return HttpResponse(template.render(context, request))
@login_required
def languageIndex(request):
    languages = Language.objects.all()
    x = Language.objects.count()
    context ={
        'x':x,
        'languages': languages
    }
    template = loader.get_template('language/index.html')
    return HttpResponse(template.render(context, request))
@login_required
def addLanguageProc(request):
    languageName = request.POST['language']
    code = request.POST['code']
    image = request.FILES.get('flag')
    language = Language(
        language_name = languageName,
        language_code = code,
        language_image = image
    )
    language.save()
    LogEntryAdd(request.session['id'], language, '', '', languageName)
    messages.success(request,languageName + ' added successfully !!!')
    return HttpResponseRedirect(reverse('languageIndex'))
@login_required
def addBook(request):
    book_name = request.POST['book_name']
    book_released = request.POST['book_released']
    language = request.POST['language']
    description = request.POST['description']
    image = request.FILES.get('image')
    publisher = request.POST['publisher']
    author = request.POST.getlist('author')
    subgenre = request.POST.getlist('subgenre')
    theme = request.POST.getlist('theme')
    book_amount=request.POST['book_amount']
    book_pages=request.POST['book_page']
    book = Books(
        book_name=book_name,
        book_image=image,
        book_description=description,
        book_language=Language.objects.get(language_id=language),
        book_publisher=Publisher.objects.get(publisher_id=publisher),
        book_released=book_released,
        book_amount=book_amount,
        book_pages=book_pages
    )
    book.save()
    LastInsertId = Books.objects.latest()
    for authorId in author:
        bookAuthor = BookAuthorship(
            bookauthorship_bookId = Books.objects.get(book_id=LastInsertId.book_id),
            bookauthorship_authorId = Authors.objects.get(author_id=authorId)
        )
        bookAuthor.save()
    for subgenreId in subgenre:
        bookSubGenre = BookSubGenre(
            booksubgenre_bookId = Books.objects.get(book_id=LastInsertId.book_id),
            booksubgenre_subgenreId = SubGenre.objects.get(id = subgenreId)
        )
        bookSubGenre.save()
    for themeId in theme:
        bookTheme = BookThemes(
            bookthemes_bookId = Books.objects.get(book_id=LastInsertId.book_id),
            bookthemes_themeId = Themes.objects.get(theme_id= themeId)
        )
        bookTheme.save()
    return HttpResponseRedirect(reverse('booksIndex'))
@login_required
def edit(request,id):
    books = Books.objects.all().prefetch_related('book_Authorship_bookId','book_Subgenre_bookId','book_Themes_bookId').get(book_id = id)
    publishers = Publisher.objects.all().prefetch_related().select_related()
    languages = Language.objects.all()
    subgenres = SubGenre.objects.all().select_related('subgenre_ofGenre').order_by('subgenre_ofGenre_id')
    themes = Themes.objects.all()
    authors = Authors.objects.all()
    template = loader.get_template('books/edit.html')
    context = {
        'books' : books,
        'publishers': publishers,
        'languages': languages,
        'subgenres': subgenres,
        'themes': themes,
        'authors': authors
    }
    return HttpResponse(template.render(context,request))
@login_required
def update(request,id):
    book_name = request.POST['book_name']
    book_released = request.POST['book_released']
    language = request.POST['languageSelectEdit']
    description = request.POST['description']
    image = request.FILES.get('image')
    publisher = request.POST['publisherSelect']
    author = request.POST.getlist('authorSelectEdit')
    subgenre = request.POST.getlist('subgenreSelectEdit')
    theme = request.POST.getlist('themeSelectEdit')
    book_amount=request.POST['book_amount']
    book_pages=request.POST['book_page']
    book = Books.objects.get(book_id=id)
    if image is None:
        book.book_name= book_name
        book.book_description = description
        book.book_language = Language.objects.get(language_id=language)
        book.book_publisher = Publisher.objects.get(publisher_id=publisher)
        book.book_released = book_released
        book.book_amount = book_amount
        book.book_pages = book_pages
    else:
        book.book_name= book_name
        book.book_image = image
        book.book_description = description
        book.book_language = Language.objects.get(language_id=language)
        book.book_publisher = Publisher.objects.get(publisher_id=publisher)
        book.book_released = book_released
        book.book_amount = book_amount
        book.book_pages = book_pages
    book.save()
    BookAuthorship.objects.filter(bookauthorship_bookId=id).delete()
    BookSubGenre.objects.filter(booksubgenre_bookId=id).delete()
    BookThemes.objects.filter(bookthemes_bookId=id).delete()
    for authorId in author:
        bookAuthor = BookAuthorship(
            bookauthorship_bookId = Books.objects.get(book_id=id),
            bookauthorship_authorId = Authors.objects.get(author_id=authorId)
        )
        bookAuthor.save()
    for subgenreId in subgenre:
        bookSubGenre = BookSubGenre(
            booksubgenre_bookId = Books.objects.get(book_id=id),
            booksubgenre_subgenreId = SubGenre.objects.get(id = subgenreId)
        )
        bookSubGenre.save()
    for themeId in theme:
        bookTheme = BookThemes(
            bookthemes_bookId = Books.objects.get(book_id=id),
            bookthemes_themeId = Themes.objects.get(theme_id= themeId)
        )
        bookTheme.save()
    return HttpResponseRedirect(reverse('booksIndex'))