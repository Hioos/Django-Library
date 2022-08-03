import datetime
import logging
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.template import loader

from apps.accounts.models import Account
from apps.authors.models import Authors
from apps.book.models import Books, LoanedBook, Receipt
from apps.genre.models import Genre, Themes, SubGenre
from apps.loan.models import loanStatus


def index(request):
    cart = []
    books = Books.objects.raw('SELECT * FROM book_books LEFT JOIN (SELECT loanedBook_book_id,count(*) as asd FROM book_loanedbook WHERE loanedBook_statusId_id = 2 OR loanedBook_statusId_id = 3 OR loanedBook_statusId_id = 6 GROUP BY loanedBook_book_id) ON loanedBook_book_id = book_id ORDER BY book_id DESC')
    lists = Genre.objects.all()
    authors = Authors.objects.all()
    newbooks = Books.objects.all().order_by('-book_id')[:6]
    shortStories = Books.objects.filter(book_pages__lte=100).order_by('-book_id')[:6]
    themes = Themes.objects.all()
    template = loader.get_template('userIndex/index.html')
    count = 0
    hot = Books.objects.raw('SELECT * FROM book_books LEFT JOIN (SELECT loanedBook_book_id,count(*) as asd FROM book_loanedbook GROUP BY loanedBook_book_id) ON loanedBook_book_id = book_id ORDER BY asd DESC')[:6]
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1

    context = {
        'cart': cart,
        'books': books,
        'lists': lists,
        'themes': themes,
        'newbooks': newbooks,
        'authors': authors,
        'count': count,
        'hot': hot,
        'shortStories' : shortStories,
    }
    return HttpResponse(template.render(context, request))


def bookInfo(request, id):
    cart = []
    book = Books.objects.prefetch_related('book_Authorship_bookId', 'book_Subgenre_bookId', 'book_Themes_bookId').get(
        book_id=id)
    allbooks = Books.objects.prefetch_related('book_Authorship_bookId', 'book_Subgenre_bookId',
                                              'book_Themes_bookId').exclude(book_id=id).order_by('-book_id')[:4]
    lists = Genre.objects.all()
    themes = Themes.objects.all()
    usedBook = LoanedBook.objects.filter(
        Q(loanedBook_book_id=id) & (Q(loanedBook_statusId_id=6) | Q(loanedBook_statusId_id=3))).count()
    left = book.book_amount - usedBook
    template = loader.get_template('userIndex/book_info.html')
    count = 0
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1

    mtfk = 0
    for product in cart:
        currentId = product.get('id')
        if book.book_id == currentId:
            mtfk = mtfk + 1
    context = {
        'book': book,
        'lists': lists,
        'themes': themes,
        'allbooks': allbooks,
        'left': left,
        'cart': cart,
        'count': count,
        'mtfk': mtfk
    }
    return HttpResponse(template.render(context, request))


def bookList(request, id):
    cart = []
    sub_Genre = SubGenre.objects.filter(subgenre_ofGenre=id).all()
    genre = Genre.objects.get(id=id)
    lists = Genre.objects.all()
    themes = Themes.objects.all()
    strid = str(id)
    books = Books.objects.raw(
        'SELECT * FROM book_books INNER JOIN book_booksubgenre ON book_id = book_booksubgenre.booksubgenre_bookId_id INNER JOIN genre_subgenre ON book_booksubgenre.booksubgenre_subgenreId_id = genre_subgenre.id INNER JOIN genre_genre ON subgenre_ofGenre_id = genre_genre.id WHERE genre_genre.id = %s GROUP BY book_name ORDER BY book_id DESC',
        [strid])
    x = len(list(books))
    template = loader.get_template('userIndex/list.html')
    count = 0
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1

    context = {
        'cart': cart,
        'genre': genre,
        'lists': lists,
        'themes': themes,
        'sub_Genre': sub_Genre,
        'books': books,
        'x': x,
        'count': count,

    }
    return HttpResponse(template.render(context, request))


def themeInfo(request, id):
    strid = str(id)
    cart = []
    bookThemes = Books.objects.raw(
        'SELECT * FROM book_books INNER JOIN book_bookthemes ON book_books.book_id = book_bookthemes.bookthemes_bookId_id WHERE bookthemes_themeId_id = %s',
        [strid])
    themedesc = Themes.objects.get(theme_id=id)
    themes = Themes.objects.all()
    lists = Genre.objects.all()
    x = len(list(bookThemes))
    template = loader.get_template('userIndex/themes.html')
    count = 0
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1
    context = {
        'themes': themes,
        'lists': lists,
        'bookThemes': bookThemes,
        'themedesc': themedesc,
        'count': count,
        'x': x

    }
    return HttpResponse(template.render(context, request))


def addtoCart(request):
    data = request.GET['catid']
    book = Books.objects.prefetch_related('book_Authorship_bookId').get(book_id=data)
    cart = []
    if "cart" in request.session:
        cart = request.session['cart']
    inCart = False
    for product in cart:
        currentId = product.get('id')
        if currentId == book.book_id:
            inCart = True
    if inCart == False:
        cart.append({
            'id': book.book_id,
            'name': book.book_name,
        })
    request.session['cart'] = cart
    return redirect('cart')


def clearCart(request):
    del request.session['cart']
    return redirect('cart')


def cart(request):
    cart = None
    if "cart" in request.session:
        cart = request.session['cart']
    template = loader.get_template('userIndex/cart.html')
    x = datetime.datetime.today()
    themes = Themes.objects.all()
    lists = Genre.objects.all()
    count = 0
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1
    context = {
        'cart': cart,
        'x': x,
        'themes': themes,
        'lists': lists,
        'count': count,
    }
    return HttpResponse(template.render(context, request))


def deleteCart(request, id):
    cart = []
    if "cart" in request.session:
        cart = request.session['cart']
    updatedCart = []
    for cartProduct in cart:
        currentId = cartProduct.get('id')
        if currentId != id:
            updatedCart.append(cartProduct)
    request.session['cart'] = updatedCart
    return redirect('cart')


def requestBook(request):
    booksId = request.POST.getlist('bookId')
    error = 0
    failed = []
    for book in booksId:
        usedBook = LoanedBook.objects.filter(
            Q(loanedBook_book_id=book) & (Q(loanedBook_statusId_id=6) | Q(loanedBook_statusId_id=3))).count()
        bookAmount = Books.objects.get(book_id=book)
        if bookAmount.book_amount - usedBook <= 0:
            error = error + 1
            failed.append(bookAmount.book_name)
    if error == 0:
        book_receipt = Receipt(
            receipt_user_id=request.session['id']
        )
        book_receipt.save()
        LastInsertId = Receipt.objects.latest()
        for book in booksId:
            inStart = request.POST['dateStart' + book]
            inDue = request.POST['dateDue' + book]
            loaned_book = LoanedBook(
                loanedBook_startDate=inStart,
                loanedBook_dueDate=inDue,
                loanedBook_book_id=book,
                loanedBook_receipt_id=LastInsertId.receipt_id,
                loanedBook_statusId=loanStatus.objects.get(loanStatus_id=4)
            )
            loaned_book.save()
        del request.session['cart']
        messages.success(request, 'Requested !!! Please wait until Librarians Accept your Request !')
        return redirect('indexOfUser')
    else:
        for fail in failed:
            messages.success(request, fail + " Not Enough in Library")
        return redirect('cart')

def allBook(request):
    cart = []
    books = Books.objects.all().prefetch_related('book_Authorship_bookId', 'book_Subgenre_bookId',
                                                 'book_Themes_bookId').order_by('-book_id')
    lists = Genre.objects.all()
    authors = Authors.objects.all()
    newbooks = Books.objects.raw('SELECT * FROM book_books LEFT JOIN (SELECT loanedBook_book_id,count(*) as asd FROM book_loanedbook WHERE loanedBook_statusId_id = 2 OR loanedBook_statusId_id = 3 OR loanedBook_statusId_id = 6 GROUP BY loanedBook_book_id) ON loanedBook_book_id = book_id ORDER BY book_id DESC')
    themes = Themes.objects.all()
    template = loader.get_template('userIndex/all_book.html')
    sub_Genre = SubGenre.objects.all()
    x = len(list(newbooks))
    count = 0
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1
    context = {
        'cart': cart,
        'books': books,
        'lists': lists,
        'themes': themes,
        'newbooks': newbooks,
        'x':x,
        'authors': authors,
        'sub_Genre':sub_Genre,
        'count': count
    }
    return HttpResponse(template.render(context, request))

def information(request):
    if "name" in request.session:
        cart = []
        id = request.session['id']
        lists = Genre.objects.all()
        themes = Themes.objects.all()
        count = 0
        information = Account.objects.get(id=id)
        if "cart" in request.session:
            cart = request.session['cart']
            for cartProduct in cart:
                count = count + 1
        context={
            'cart': cart,
            'information' : information,
            'lists': lists,
            'themes': themes,
            'count': count
        }
        template = loader.get_template('userIndex/information.html')
        return HttpResponse(template.render(context, request))
    else:
        return redirect('indexOfUser')

def history(request):
    cart = []
    id = request.session['id']
    lists = Genre.objects.all()
    themes = Themes.objects.all()
    count = 0
    loans = loanStatus.objects.all()
    receipts = Receipt.objects.prefetch_related().filter(receipt_user=id).order_by('-receipt_id')
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1
    context = {
        'cart': cart,
        'lists': lists,
        'loans': loans,
        'receipts':receipts,
        'themes': themes,
        'count': count
    }
    template = loader.get_template('userIndex/history.html')
    return HttpResponse(template.render(context, request))