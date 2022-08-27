import datetime
import logging
import math

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.template import loader

from apps.accounts.models import Account, Pricing, PaymentHistory
from apps.authors.models import Authors
from apps.book.models import Books, LoanedBook, Receipt, DetailedBook
from apps.genre.models import Genre, Themes, SubGenre
from apps.loan.models import loanStatus


def index(request):
    cart = []
    books = Books.objects.raw(
        'SELECT *,COUNT(detailed_book_id_id) as asd,COUNT(case when detailed_returned = 1 then 1 else null end ) as returned FROM book_detailedbook INNER JOIN book_books ON detailed_book_id_id=book_id GROUP BY detailed_book_id_id ORDER BY book_id DESC')
    lists = Genre.objects.all()
    authors = Authors.objects.all()
    newbooks = Books.objects.all().order_by('-book_id')[:6]
    shortStories = Books.objects.filter(book_pages__lte=100).order_by('-book_id')[:6]
    themes = Themes.objects.all()
    template = loader.get_template('userIndex/index.html')
    count = 0
    if 'id' not in request.session:
        strid = None
    else:
        strid = str(request.session['id'])
    hot = Books.objects.raw(
        "SELECT *,COUNT(detailed_book_id_id) as total FROM book_detailedbook LEFT JOIN book_loanedbook ON loanedBook_book_id = detailed_id INNER JOIN book_books ON detailed_book_id_id = book_books.book_id WHERE loanedBook_id NOTNULL AND loanedBook_returnedStatus !=5 AND loanedBook_startDate > DATETIME('now', '-7 day')  GROUP BY detailed_book_id_id ORDER BY total DESC LIMIT 6")[
          :6]
    forYou = LoanedBook.objects.raw("SELECT *,COUNT(loanedBook_id) as d,genre_genre.id as sad FROM book_loanedbook INNER JOIN book_receipt on book_loanedbook.loanedBook_receipt_id=book_receipt.receipt_id INNER JOIN accounts_account ON book_receipt.receipt_user_id = accounts_account.id INNER JOIN book_detailedbook ON detailed_id = book_loanedbook.loanedBook_book_id INNER JOIN book_books ON detailed_book_id_id = book_id INNER JOIN book_booksubgenre ON book_id = book_booksubgenre.booksubgenre_bookId_id INNER JOIN genre_subgenre ON booksubgenre_subgenreId_id = genre_subgenre.id INNER JOIN genre_genre On genre_subgenre.subgenre_ofGenre_id = genre_genre.id WHERE accounts_account.id = %s GROUP BY genre_subgenre.id ORDER BY d DESC LIMIT 1",[strid])
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1
    d = None
    for f in forYou:
        d = str(f.sad)
    forYouBooks = Books.objects.raw('SELECT * FROM book_books LEFT JOIN (SELECT count(detailed_returned) as returned,detailed_book_id_id FROM book_detailedbook WHERE detailed_returned = 1 GROUP BY detailed_book_id_id) ON book_books.book_id = detailed_book_id_id INNER JOIN book_booksubgenre ON book_booksubgenre.booksubgenre_bookId_id = book_id INNER JOIN genre_subgenre ON book_booksubgenre.booksubgenre_subgenreId_id = genre_subgenre.id WHERE subgenre_ofGenre_id = %s GROUP BY book_id ORDER BY book_id DESC',[d])
    context = {
        'cart': cart,
        'books': books,
        'lists': lists,
        'forYou': forYou,
        'themes': themes,
        'forYouBooks': forYouBooks,
        'newbooks': newbooks,
        'authors': authors,
        'count': count,
        'hot': hot,
        'shortStories': shortStories,
    }
    return HttpResponse(template.render(context, request))


def bookInfo(request, id):
    cart = []
    book = Books.objects.prefetch_related('book_Authorship_bookId', 'book_Subgenre_bookId', 'book_Themes_bookId').get(
        book_id=id)
    allbooks = Books.objects.prefetch_related('book_Authorship_bookId', 'book_Subgenre_bookId',
                                              'book_Themes_bookId').exclude(book_id=id).order_by('-book_id')[:12]
    details = DetailedBook.objects.filter(detailed_book_id=book.book_id,detailed_book_percentage__range=(10, 100))
    lists = Genre.objects.all()
    themes = Themes.objects.all()
    usedBook = LoanedBook.objects.filter(
        Q(loanedBook_book_id=id) & (Q(loanedBook_statusId_id=6))).count()
    template = loader.get_template('userIndex/book_info.html')
    count = 0
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1
    strid = str(id)
    stridUser = 0
    if "id" in request.session:
        stridUser = str(request.session['id'])
    read = Books.objects.raw('SELECT * FROM book_books INNER JOIN book_detailedbook ON book_id = detailed_book_id_id INNER JOIN book_loanedbook ON loanedBook_book_id = detailed_id INNER JOIN book_receipt ON loanedBook_receipt_id = receipt_id WHERE receipt_user_id = '+stridUser+' and book_id = '+strid+' GROUP BY book_id')
    mtfk = 0
    for product in cart:
        currentId = product.get('id')
        if book.book_id == currentId:
            mtfk = mtfk + 1
    context = {
        'book': book,
        'lists': lists,
        'read':read,
        'themes': themes,
        'allbooks': allbooks,
        'cart': cart,
        'details': details,
        'count': count,
        'mtfk': mtfk
    }
    return HttpResponse(template.render(context, request))


def bookList(request, id):
    cart = []
    sub_Genres = SubGenre.objects.filter(subgenre_ofGenre=id).all().order_by('?')
    genre = Genre.objects.get(id=id)
    lists = Genre.objects.all()
    themes = Themes.objects.all()
    strid = str(id)
    book = Books.objects.raw(
        'SELECT *,COUNT(detailed_book_id_id) as asd,COUNT(case when detailed_returned = 1 then 1 else null end ) as returned FROM book_detailedbook INNER JOIN book_books ON detailed_book_id_id=book_id INNER JOIN book_booksubgenre ON book_id = book_booksubgenre.booksubgenre_bookId_id INNER JOIN genre_subgenre ON book_booksubgenre.booksubgenre_subgenreId_id = genre_subgenre.id INNER JOIN genre_genre ON subgenre_ofGenre_id = genre_genre.id WHERE genre_genre.id = %s GROUP BY book_name ORDER BY book_id DESC',
        [strid])
    x = len(list(book))
    template = loader.get_template('userIndex/list.html')
    count = 0
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1
    page = request.GET.get('page', 1)
    paginator = Paginator(book, 12)
    paginator2 = Paginator(sub_Genres,12)
    try:
        books = paginator.page(page)
        sub_Genre = paginator2.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
        sub_Genre = paginator2.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
        sub_Genre = paginator2.page(paginator.num_pages)

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
    bookTheme = Books.objects.raw(
        'SELECT *,COUNT(detailed_book_id_id) as asd,COUNT(case when detailed_returned = 1 then 1 else null end ) as returned FROM book_detailedbook INNER JOIN book_books ON detailed_book_id_id=book_id INNER JOIN book_bookthemes ON book_id = book_bookthemes.bookthemes_bookId_id INNER JOIN genre_themes ON bookthemes_themeId_id = genre_themes.theme_id WHERE genre_themes.theme_id = %s GROUP BY book_name ORDER BY book_id DESC ',
        [strid])
    x = len(list(bookTheme))
    themedesc = Themes.objects.get(theme_id=id)
    page = request.GET.get('page', 1)
    paginator = Paginator(bookTheme, 12)
    try:
        bookThemes = paginator.page(page)
    except PageNotAnInteger:
        bookThemes = paginator.page(1)
    except EmptyPage:
        bookThemes = paginator.page(paginator.num_pages)
    themes = Themes.objects.all()
    lists = Genre.objects.all()

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
    bookDetail = DetailedBook.objects.get(detailed_id = data)
    book = Books.objects.prefetch_related('book_Authorship_bookId').get(book_id=bookDetail.detailed_book_id_id)
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
            'bcode': bookDetail.detailed_id
        })
    request.session['cart'] = cart
    return redirect('cart')


def clearCart(request):
    del request.session['cart']
    return redirect('cart')


def cart(request):
    user_id = request.session['id']
    user = Account.objects.get(id = user_id)
    mindate = user.expired_date - datetime.timedelta(days=3)
    today = datetime.date.today()
    if mindate > today:
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
            'user':user,
            'mindate':mindate,
            'themes': themes,
            'lists': lists,
            'count': count,
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.success(request, "Please extends your membership first")
        return redirect('extend')


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
    books = request.POST.getlist('bookId')
    error = 0
    failed = []
    account = Account.objects.get(id=request.session['id'])
    if account.is_available is True:
        for book in books:
            strid = str(book)
            book_amount = DetailedBook.objects.raw('SELECT *,COUNT(detailed_id) as amount FROM book_detailedbook INNER JOIN book_books ON detailed_book_id_id = book_id WHERE detailed_id = %s',[strid])
            usedBook = LoanedBook.objects.filter(
                Q(loanedBook_book_id=book) & (Q(loanedBook_statusId_id=6) | Q(loanedBook_statusId_id=3) | Q(
                    loanedBook_statusId_id=8))).count()
            book_amount[0].amount
            for x in book_amount:
                if x.amount - usedBook <= 0:
                    error = error + 1
                    failed.append(x.book_name)
        if error == 0:
            for book in books:
                strid = str(book)
                book_amount = DetailedBook.objects.raw(
                    'SELECT *,COUNT(detailed_id) as amount FROM book_detailedbook INNER JOIN book_books ON detailed_book_id_id = book_id WHERE detailed_id = %s',
                    [strid])
                for x in book_amount:
                    x.detailed_returned = False
                    x.save()
            book_receipt = Receipt(
                receipt_user_id=request.session['id']
            )
            book_receipt.save()
            LastInsertId = Receipt.objects.latest()
            for book in books:
                inStart = request.POST['dateStart' + book]
                inDue = request.POST['dateDue' + book]
                loaned_book = LoanedBook(
                    loanedBook_startDate=inStart,
                    loanedBook_dueDate=inDue,
                    loanedBook_book_id=book,
                    loanedBook_receipt_id=LastInsertId.receipt_id,
                    loanedBook_statusId=loanStatus.objects.get(loanStatus_id=4  )
                )
                loaned_book.save()
            del request.session['cart']
            messages.success(request, ('Done !!! Please wait for out librarians to confirm your request !'))
            return redirect('indexOfUser')
        else:
            for fail in failed:
                messages.success(request, (fail + ' Is not enough in Library !!!'))
            return redirect('cart')
    else:
        messages.success(request, ('You are already borrowing books !!!'))
        return redirect('cart')

def allBook(request):
    cart = []
    books = Books.objects.all().prefetch_related('book_Authorship_bookId', 'book_Subgenre_bookId',
                                                 'book_Themes_bookId').order_by('-book_id')
    lists = Genre.objects.all()
    authors = Authors.objects.all()
    newbook = Books.objects.raw(
        'SELECT *,COUNT(detailed_book_id_id) as asd,COUNT(case when detailed_returned = 1 then 1 else null end ) as returned FROM book_detailedbook INNER JOIN book_books ON detailed_book_id_id=book_id GROUP BY detailed_book_id_id ORDER BY book_id DESC')
    themes = Themes.objects.all()
    template = loader.get_template('userIndex/all_book.html')
    sub_Genres = SubGenre.objects.all().order_by('?')
    x = len(list(newbook))
    count = 0
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1
    page = request.GET.get('page', 1)
    paginator = Paginator(newbook, 12)
    pagNumber = x / 12
    pagS = len(list(sub_Genres)) / math.ceil(pagNumber)
    pagSub = math.ceil(pagS)
    paginator2 = Paginator(sub_Genres,pagSub)
    try:
        newbooks = paginator.page(page)
        sub_Genre = paginator2.page(page)
    except PageNotAnInteger:
        newbooks = paginator.page(1)
        sub_Genre = paginator2.page(1)
    except EmptyPage:
        newbooks = paginator.page(paginator.num_pages)
        sub_Genre = paginator2.page(paginator.num_pages)
    context = {
        'cart': cart,
        'books': books,
        'lists': lists,
        'themes': themes,
        'newbooks': newbooks,
        'x': x,
        'authors': authors,
        'sub_Genre': sub_Genre,
        'count': count
    }
    return HttpResponse(template.render(context, request))
# hahaha

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
        context = {
            'cart': cart,
            'information': information,
            'lists': lists,
            'themes': themes,
            'count': count
        }
        template = loader.get_template('userIndex/information.html')
        return HttpResponse(template.render(context, request))
    else:
        return redirect('indexOfUser')


def history(request):
    if "name" in request.session:
        cart = []
        id = request.session['id']
        strid = str(id)
        lists = Genre.objects.all()
        themes = Themes.objects.all()
        count = 0
        today = datetime.date.today()
        loans = loanStatus.objects.all()
        inuse = LoanedBook.objects.raw('SELECT * FROM book_loanedbook INNER JOIN book_detailedbook ON loanedBook_book_id = detailed_id INNER JOIN book_books ON book_detailedbook.detailed_book_id_id = book_books.book_id INNER JOIN book_receipt ON loanedBook_receipt_id = book_receipt.receipt_id INNER JOIN accounts_account ON receipt_user_id = accounts_account.id WHERE receipt_user_id= %s AND (loanedBook_statusId_id = 6 OR loanedBook_statusId_id=2)',[strid])
        payments = PaymentHistory.objects.prefetch_related().filter(user_id=id).order_by('-history_Id')
        receipts = Receipt.objects.prefetch_related().filter(receipt_user=id).order_by('-receipt_id')
        if "cart" in request.session:
            cart = request.session['cart']
            for cartProduct in cart:
                count = count + 1
        context = {
            'inuse': inuse,
            'today':today,
            'cart': cart,
            'lists': lists,
            'loans': loans,
            'receipts': receipts,
            'themes': themes,
            'count': count,
            'payments': payments
        }
        template = loader.get_template('userIndex/history.html')
        return HttpResponse(template.render(context, request))
    else:
        return redirect('indexOfUser')

def extend(request):
    cart = []
    lists = Genre.objects.all()
    themes = Themes.objects.all()
    count = 0
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1
    pricings = Pricing.objects.filter(pricing_price__gte=0.4).order_by('pricing_price')
    template = loader.get_template('userIndex/extend.html')
    context = {
        'lists': lists,
        'cart': cart,
        'count': count,
        'themes': themes,
        'pricings': pricings
    }
    return HttpResponse(template.render(context, request))


def extendInfo(request, id):
    if "name" in request.session:
        cart = []
        lists = Genre.objects.all()
        themes = Themes.objects.all()
        count = 0
        pricings = Pricing.objects.get(pricing_id=id)
        user = Account.objects.get(id=request.session['id'])
        template = loader.get_template('userIndex/extendInfo.html')
        current = user.expired_date
        after = current + datetime.timedelta(days=pricings.pricing_days)
        if "cart" in request.session:
            cart = request.session['cart']
            for cartProduct in cart:
                count = count + 1
        context = {
            'lists': lists,
            'cart': cart,
            'count': count,
            'themes': themes,
            'pricings': pricings,
            'user': user,
            'after': after
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('indexOfUser')

def extendMember(request, id):
    # data = request.GET['catid']
    if "name" in request.session:
        pricing = Pricing.objects.get(pricing_id=id)
        user = Account.objects.get(id=request.session['id'])
        days = pricing.pricing_days
        history = PaymentHistory(
            user_id=user,
            pricing=pricing,
            old_expired_date = user.expired_date,
            new_expired_date = user.expired_date + datetime.timedelta(days=days)
        )
        history.save()
        user.expired_date = user.expired_date + datetime.timedelta(days=days)
        user.save()
        messages.success(request, "Done")
        return redirect('history')
    else:
        return redirect('indexOfUser')
def search(request):
    cart = []
    lists = Genre.objects.all()
    searchText = request.GET['search']
    newbook = Books.objects.filter(book_name__contains = searchText)
    template = loader.get_template('userIndex/search.html')
    themes = Themes.objects.all()
    sub_Genre = SubGenre.objects.all()
    x = len(list(newbook))
    count = 0
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1
    page = request.GET.get('page', 1)
    paginator = Paginator(newbook, 12)
    try:
        newbooks = paginator.page(page)
    except PageNotAnInteger:
        newbooks = paginator.page(1)
    except EmptyPage:
        newbooks = paginator.page(paginator.num_pages)

    context = {
        'lists':lists,
        'cart': cart,
        'themes': themes,
        'newbooks': newbooks,
        'x': x,
        'sub_Genre': sub_Genre,
        'count': count,
        'searchText':searchText
    }
    return HttpResponse(template.render(context, request))

def authorUser(request,id):
    cart = []
    strid = str(id)
    authors = Authors.objects.get(author_id=id)
    lists = Genre.objects.all()
    themes = Themes.objects.all()
    count = 0
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1
    template = loader.get_template('userIndex/authors.html')
    newbook = Books.objects.raw(
        'SELECT *,COUNT(detailed_book_id_id) as asd,COUNT(case when detailed_returned = 1 then 1 else null end ) as returned FROM book_detailedbook INNER JOIN book_books ON detailed_book_id_id=book_id INNER JOIN book_bookauthorship ON book_id = book_bookauthorship.bookauthorship_bookId_id WHERE bookauthorship_authorId_id=%s GROUP BY book_name ORDER BY book_id DESC',[strid])
    page = request.GET.get('page', 1)
    paginator = Paginator(newbook, 12)
    try:
        newbooks = paginator.page(page)
    except PageNotAnInteger:
        newbooks = paginator.page(1)
    except EmptyPage:
        newbooks = paginator.page(paginator.num_pages)
    subgenres= SubGenre.objects.raw('SELECT * FROM book_books INNER JOIN book_bookauthorship ON book_books.book_id=book_bookauthorship.bookauthorship_bookId_id  INNER JOIN book_booksubgenre ON book_id = book_booksubgenre.booksubgenre_bookId_id INNER JOIN genre_subgenre ON booksubgenre_subgenreId_id=genre_subgenre.id WHERE book_bookauthorship.bookauthorship_authorId_id=%s  GROUP BY booksubgenre_subgenreId_id',[strid])
    authorThemes = Themes.objects.raw('SELECT * FROM book_books INNER JOIN book_bookauthorship ON book_books.book_id=book_bookauthorship.bookauthorship_bookId_id  INNER JOIN book_bookthemes ON book_id = book_bookthemes.bookthemes_bookId_id INNER JOIN genre_themes ON theme_id=book_bookthemes.bookthemes_themeId_id WHERE book_bookauthorship.bookauthorship_authorId_id=%s  GROUP BY book_bookthemes.bookthemes_themeId_id',[strid])
    context={
        'authors':authors,
        'cart':cart,
        'lists':lists,
        'themes':themes,
        'count':count,
        'newbooks':newbooks,
        'authorThemes':authorThemes,
        'subgenres':subgenres
    }
    return HttpResponse(template.render(context, request))
def subGenreUser(request,id):
    template = loader.get_template('userIndex/sub_genre.html')
    cart = []
    strid = str(id)
    lists = Genre.objects.all()
    themes = Themes.objects.all()
    subGenres = SubGenre.objects.get(id = id)
    count = 0
    if "cart" in request.session:
        cart = request.session['cart']
        for cartProduct in cart:
            count = count + 1
    strid = str(id)
    book = Books.objects.raw(
        'SELECT *,COUNT(detailed_book_id_id) as asd,COUNT(case when detailed_returned = 1 then 1 else null end ) as returned FROM book_detailedbook INNER JOIN book_books ON detailed_book_id_id=book_id INNER JOIN book_booksubgenre ON book_id = book_booksubgenre.booksubgenre_bookId_id INNER JOIN genre_subgenre ON book_booksubgenre.booksubgenre_subgenreId_id = genre_subgenre.id WHERE genre_subgenre.id = %s GROUP BY book_name ORDER BY book_id DESC',
        [strid])
    x = len(list(book))
    page = request.GET.get('page', 1)
    paginator = Paginator(book, 12)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'subGenres': subGenres,
        'cart': cart,
        'lists': lists,
        'themes': themes,
        'count': count,
        'x':x,
        'books':books
    }
    return HttpResponse(template.render(context, request))
def contact(request):
    template = loader.get_template('userIndex/contact.html')
    return HttpResponse(template.render({}, request))