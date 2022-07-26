from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader

from apps.authors.models import Authors
from apps.book.models import Books
from apps.genre.models import Genre


def index(request):
    books = Books.objects.all().prefetch_related('book_Authorship_bookId', 'book_Subgenre_bookId','book_Themes_bookId').order_by('-book_id')
    lists = Genre.objects.all()
    authors = Authors.objects.all()
    newbooks = Books.objects.all().order_by('-book_id')[:6]
    template = loader.get_template('userIndex/index.html')
    context = {
        'books': books,
        'lists': lists,
        'newbooks': newbooks,
        'authors': authors
    }
    return HttpResponse(template.render(context, request))