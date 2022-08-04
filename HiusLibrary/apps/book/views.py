import datetime
from venv import create

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Books, Language, BookAuthorship, BookSubGenre, BookThemes, Receipt, LoanedBook
# Create your views here.
from ..accounts.models import Account
from ..authors.models import Authors
from ..genre.models import SubGenre, Themes
from ..loan.models import loanStatus
from ..publisher.models import Publisher
from datetime import date

def LogEntryAdd(idUser, modelName, objectId, reason, after):
    LogEntry.objects.log_action(
        user_id=idUser,
        content_type_id=ContentType.objects.get_for_model(modelName).pk,
        object_id=objectId,
        object_repr=reason,
        change_message=after,
        action_flag=ADDITION if create else CHANGE)


@login_required
def index(request):
    books = Books.objects.all().prefetch_related('book_Authorship_bookId', 'book_Subgenre_bookId', 'book_Themes_bookId').order_by('-book_id')

    template = loader.get_template('books/index.html')

    def bookCounter():
        count = Books.objects.all().count()
        return count

    x = bookCounter()
    context = {
        'books': books,
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
    context = {
        'publishers': publishers,
        'languages': languages,
        'subgenres': subgenres,
        'themes': themes,
        'authors': authors
    }
    template = loader.get_template('books/add.html')
    return HttpResponse(template.render(context, request))


@login_required
def languageIndex(request):
    languages = Language.objects.all()
    x = Language.objects.count()
    context = {
        'x': x,
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
        language_name=languageName,
        language_code=code,
        language_image=image
    )
    language.save()
    LogEntryAdd(request.session['id'], language, '', '', languageName)
    messages.success(request, languageName + ' added successfully !!!')
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
    book_amount = request.POST['book_amount']
    book_pages = request.POST['book_page']
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
            bookauthorship_bookId=Books.objects.get(book_id=LastInsertId.book_id),
            bookauthorship_authorId=Authors.objects.get(author_id=authorId)
        )
        bookAuthor.save()
    for subgenreId in subgenre:
        bookSubGenre = BookSubGenre(
            booksubgenre_bookId=Books.objects.get(book_id=LastInsertId.book_id),
            booksubgenre_subgenreId=SubGenre.objects.get(id=subgenreId)
        )
        bookSubGenre.save()
    for themeId in theme:
        bookTheme = BookThemes(
            bookthemes_bookId=Books.objects.get(book_id=LastInsertId.book_id),
            bookthemes_themeId=Themes.objects.get(theme_id=themeId)
        )
        bookTheme.save()
    messages.success(request, (book_name + ' Added Successfully !!!'))
    return HttpResponseRedirect(reverse('booksIndex'))


@login_required
def edit(request, id):
    books = Books.objects.all().prefetch_related('book_Authorship_bookId', 'book_Subgenre_bookId',
                                                 'book_Themes_bookId').get(book_id=id)
    publishers = Publisher.objects.all().prefetch_related().select_related()
    languages = Language.objects.all()
    subgenres = SubGenre.objects.all().select_related('subgenre_ofGenre').order_by('subgenre_ofGenre_id')
    themes = Themes.objects.all()
    authors = Authors.objects.all()
    template = loader.get_template('books/edit.html')
    context = {
        'books': books,
        'publishers': publishers,
        'languages': languages,
        'subgenres': subgenres,
        'themes': themes,
        'authors': authors
    }
    return HttpResponse(template.render(context, request))


@login_required
def update(request, id):
    book_name = request.POST['book_name']
    book_released = request.POST['book_released']
    language = request.POST['languageSelectEdit']
    description = request.POST['description']
    image = request.FILES.get('image')
    publisher = request.POST['publisherSelect']
    author = request.POST.getlist('authorSelectEdit')
    subgenre = request.POST.getlist('subgenreSelectEdit')
    theme = request.POST.getlist('themeSelectEdit')
    book_amount = request.POST['book_amount']
    book_pages = request.POST['book_page']
    book = Books.objects.get(book_id=id)
    if image is None:
        book.book_name = book_name
        book.book_description = description
        book.book_language = Language.objects.get(language_id=language)
        book.book_publisher = Publisher.objects.get(publisher_id=publisher)
        book.book_released = book_released
        book.book_amount = book_amount
        book.book_pages = book_pages
    else:
        book.book_name = book_name
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
            bookauthorship_bookId=Books.objects.get(book_id=id),
            bookauthorship_authorId=Authors.objects.get(author_id=authorId)
        )
        bookAuthor.save()
    for subgenreId in subgenre:
        bookSubGenre = BookSubGenre(
            booksubgenre_bookId=Books.objects.get(book_id=id),
            booksubgenre_subgenreId=SubGenre.objects.get(id=subgenreId)
        )
        bookSubGenre.save()
    for themeId in theme:
        bookTheme = BookThemes(
            bookthemes_bookId=Books.objects.get(book_id=id),
            bookthemes_themeId=Themes.objects.get(theme_id=themeId)
        )
        bookTheme.save()
    messages.success(request, (book_name + ' Updated Successfully !!!'))
    return HttpResponseRedirect(reverse('booksIndex'))


@login_required
def lendingPage(request):
    receipts = Receipt.objects.raw('SELECT * FROM book_receipt INNER JOIN book_loanedbook ON receipt_id = loanedBook_receipt_id WHERE loanedBook_statusId_id =1 OR loanedBook_statusId_id =2 OR loanedBook_statusId_id = 6 OR loanedBook_statusId_id = 8 GROUP BY receipt_id ORDER BY receipt_timestamp DESC')
    loanedBooks = LoanedBook.objects.all()
    pending = Receipt.objects.raw('SELECT * FROM book_receipt INNER JOIN book_loanedbook ON receipt_id = loanedBook_receipt_id WHERE loanedBook_statusId_id =4  GROUP BY receipt_id ORDER BY receipt_timestamp DESC')
    done = Receipt.objects.raw(
        'SELECT * FROM book_receipt INNER JOIN book_loanedbook ON receipt_id = loanedBook_receipt_id WHERE loanedBook_statusId_id =3     OR loanedBook_statusId_id =5 OR loanedBook_statusId_id = 7  GROUP BY receipt_id ORDER BY receipt_timestamp DESC')
    x = Receipt.objects.count()
    loans = loanStatus.objects.all()
    template = loader.get_template('lending/index.html')
    context = {
        'receipts': receipts,
        'x': x,
        'loanedBooks': loanedBooks,
        'pending': pending,
        'loans':loans,
        'done':done
    }
    return HttpResponse(template.render(context, request))


@login_required
def lendingAdd(request):
    books = Books.objects.all().prefetch_related('book_Authorship_bookId', 'book_Subgenre_bookId', 'book_Themes_bookId')
    users = Account.objects.exclude(is_banned=True)
    context = {
        'books': books,
        'users': users
    }
    template = loader.get_template('lending/add.html')
    return HttpResponse(template.render(context, request))


@login_required
def lendingAddProcess(request):
    books = request.POST.getlist('books')
    user = request.POST['user']
    error = 0
    failed = []
    for book in books:
        usedBook = LoanedBook.objects.filter(
            Q(loanedBook_book_id=book) & (Q(loanedBook_statusId_id=6) | Q(loanedBook_statusId_id=3))).count()
        bookAmount = Books.objects.get(book_id=book)
        if bookAmount.book_amount - usedBook <= 0:
            error = error + 1
            failed.append(bookAmount.book_name)
    if error == 0:
        book_receipt = Receipt(
            receipt_user_id=user
        )
        book_receipt.save()
        LastInsertId = Receipt.objects.latest()
        for book in books:
            inStart = request.POST['start' + book]
            inDue = request.POST['due' + book]
            loaned_book = LoanedBook(
                loanedBook_startDate=inStart,
                loanedBook_dueDate=inDue,
                loanedBook_book_id=book,
                loanedBook_receipt_id=LastInsertId.receipt_id,
                loanedBook_statusId=loanStatus.objects.get(loanStatus_id=6)
            )
            loaned_book.save()
        return HttpResponseRedirect(reverse('lendingPage'))
    else:
        for fail in failed:
            messages.success(request, (fail + 'Is not enough in Library !!!'))
        return HttpResponseRedirect(reverse('lendingAdd'))
@login_required
def acceptAll(request,id):
    admin = Account.objects.get(id = request.session['id'])
    loanedBook = LoanedBook.objects.filter(loanedBook_receipt_id=id).only('loanedBook_statusId_id')
    user = LoanedBook.objects.raw('SELECT * FROM book_loanedbook INNER JOIN book_receipt ON loanedBook_receipt_id = book_receipt.receipt_id INNER JOIN accounts_account ON receipt_user_id = accounts_account.id WHERE loanedBook_receipt_id = 45 LIMIT 1')
    for book in loanedBook:
        book.loanedBook_statusId_id = 8
        book.save()
    for x in user:
        subject = 'Thank you for using HiusLibrary'
        message = f'Dear {x.name}, \n' \
                  f'Thank you for using HiusLibrary. \n' \
                  f'Our books are waiting for you to bring them home \n' \
                  f'Please bring your ID card to our librarians at ... \n' \
                  f'\t\t\t Sincerely, \n' \
                  f'\t\t\t {admin.name}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [x.email, ]
        send_mail(subject, message, email_from, recipient_list)
    return HttpResponseRedirect(reverse('lendingPage'))
@login_required
def denyAll(request,id):
    loanedBook = LoanedBook.objects.filter(loanedBook_receipt_id=id).only('loanedBook_statusId_id')
    for book in loanedBook:
        book.loanedBook_statusId_id = 5
        book.loanedBook_dueDate = None
        book.loanedBook_startDate = None
        book.save()
    return HttpResponseRedirect(reverse('lendingPage'))
@login_required
def lendingAction(request):
    books = request.POST.getlist('bookInReceipts')
    for book in books:
        bookReceipt = LoanedBook.objects.get(loanedBook_id = book)
        selected = request.POST['selectStatus' + book]
        bookReceipt.loanedBook_statusId_id = selected
        today = datetime.datetime.today()
        bookReceipt.loanedBook_returnedDate = today
        bookReceipt.save()
    return HttpResponseRedirect(reverse('lendingPage'))
