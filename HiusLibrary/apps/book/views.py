import datetime
from venv import create

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Books, Language, BookAuthorship, BookSubGenre, BookThemes, Receipt, LoanedBook, \
    DetailedBook
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
    # books = Books.objects.all().prefetch_related('book_Authorship_bookId', 'book_Subgenre_bookId', 'book_Themes_bookId','id_of_book').annotate(total=Count('book_id')).order_by('-book_id')
    books = Books.objects.raw('SELECT *,COUNT(detailed_book_id_id) as amount FROM book_books LEFT JOIN book_detailedbook ON book_id = detailed_book_id_id GROUP BY detailed_book_id_id ORDER BY book_id DESC')
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
    book_price = request.POST['book_price']
    book = Books(
        book_name=book_name,
        book_image=image,
        book_description=description,
        book_language=Language.objects.get(language_id=language),
        book_publisher=Publisher.objects.get(publisher_id=publisher),
        book_released=book_released,
        book_pages=book_pages,
        book_price = book_price
    )
    book.save()
    LastInsertId = Books.objects.latest()
    for amount in range(int(book_amount)):
        detailedBook = DetailedBook(
            detailed_book_percentage = 100,
            detailed_book_id = Books.objects.get(book_id=LastInsertId.book_id),
            detailed_book_note = 'Good Condition',
            detailed_returned = True,
            detailed_importDate = datetime.date.today()
        )
        detailedBook.save()
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
    book_pages = request.POST['book_page']
    book = Books.objects.get(book_id=id)
    if image is None:
        book.book_name = book_name
        book.book_description = description
        book.book_language = Language.objects.get(language_id=language)
        book.book_publisher = Publisher.objects.get(publisher_id=publisher)
        book.book_released = book_released
        book.book_pages = book_pages
    else:
        book.book_name = book_name
        book.book_image = image
        book.book_description = description
        book.book_language = Language.objects.get(language_id=language)
        book.book_publisher = Publisher.objects.get(publisher_id=publisher)
        book.book_released = book_released
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
    receipts = Receipt.objects.raw('SELECT * FROM book_receipt INNER JOIN book_loanedbook ON receipt_id = loanedBook_receipt_id WHERE loanedBook_statusId_id =1 OR loanedBook_statusId_id =2 OR loanedBook_statusId_id = 6 GROUP BY receipt_id ORDER BY receipt_timestamp DESC')
    loanedBooks = LoanedBook.objects.all()
    pending = Receipt.objects.raw('SELECT * FROM book_receipt INNER JOIN book_loanedbook ON receipt_id = loanedBook_receipt_id WHERE loanedBook_statusId_id =4  GROUP BY receipt_id ORDER BY receipt_timestamp DESC')
    done = Receipt.objects.raw(
        'SELECT * FROM book_receipt INNER JOIN book_loanedbook ON receipt_id = loanedBook_receipt_id WHERE loanedBook_statusId_id =3     OR loanedBook_statusId_id =5 OR loanedBook_statusId_id = 7  GROUP BY receipt_id ORDER BY receipt_timestamp DESC')
    waits = Receipt.objects.raw(
        'SELECT * FROM book_receipt INNER JOIN book_loanedbook ON receipt_id = loanedBook_receipt_id WHERE loanedBook_statusId_id = 8 GROUP BY receipt_id ORDER BY receipt_timestamp DESC')
    x = Receipt.objects.count()
    loans = loanStatus.objects.all()
    template = loader.get_template('lending/index.html')
    context = {
        'receipts': receipts,
        'x': x,
        'loanedBooks': loanedBooks,
        'pending': pending,
        'loans':loans,
        'done':done,
        'waits':waits
    }
    return HttpResponse(template.render(context, request))


@login_required
def lendingAdd(request):
    books = DetailedBook.objects.raw('SELECT * FROM book_detailedbook INNER JOIN book_books ON book_id = detailed_book_id_id  ORDER BY book_id DESC')
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
    active = 0
    account = Account.objects.get(id=user)
    if account.is_available is False:
        active = 1
    if active == 0:
        for book in books:
            strid = str(book)
            book_amount = DetailedBook.objects.raw('SELECT *,COUNT(detailed_id) as amount FROM book_detailedbook INNER JOIN book_books ON detailed_book_id_id = book_id WHERE detailed_id = %s',[strid])
            usedBook = LoanedBook.objects.filter(
                Q(loanedBook_book_id=book) & (Q(loanedBook_statusId_id=6) | Q(loanedBook_statusId_id=3) | Q(loanedBook_statusId_id=8))).count()
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
            account.is_available = False
            account.save()
            return HttpResponseRedirect(reverse('lendingPage'))
        else:
            for fail in failed:
                messages.success(request, (fail + ' Is not enough in Library !!!'))
            return HttpResponseRedirect(reverse('lendingAdd'))
    else:
        messages.success(request, (account.name + ' Is already borrowing books !!!'))
        return HttpResponseRedirect(reverse('lendingAdd'))
@login_required
def acceptAll(request,id):
    loanedBook = LoanedBook.objects.filter(loanedBook_receipt_id=id).only('loanedBook_statusId_id')
    admin = Account.objects.get(id=request.session['id'])
    for book in loanedBook:
        bookId = book.loanedBook_book_id
        book.loanedBook_confirm = admin
        receiptId = book.loanedBook_receipt_id
        getUser = Receipt.objects.get(receipt_id = receiptId)
        user = getUser.receipt_user_id
        account = Account.objects.get(id = user)
        account.is_available = False
        detailedBook = DetailedBook.objects.get(detailed_id = bookId)
        detailedBook.detailed_returned = False
        book.loanedBook_statusId_id = 8
        book.save()
        detailedBook.save()
        account.save()
    subject = 'Thank you for using HiusLibrary'
    message = f'Dear {account.name}, \n' \
              f'Thank you for using HiusLibrary. \n' \
              f'Our books are waiting for you to bring them home \n' \
              f'Please bring your ID card to our librarians at ... \n' \
              f'\t\t\t Sincerely, \n' \
              f'\t\t\t {admin.name}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [account.email, ]
    send_mail(subject, message, email_from, recipient_list)
    messages.success(request, ('Done!!!'))
    return HttpResponseRedirect(reverse('lendingPage'))
@login_required
def denyAll(request,id):
    loanedBook = LoanedBook.objects.filter(loanedBook_receipt_id=id).only('loanedBook_statusId_id')
    for book in loanedBook:
        bookId = book.loanedBook_book_id
        receiptId = book.loanedBook_receipt_id
        getUser = Receipt.objects.get(receipt_id = receiptId)
        user = getUser.receipt_user_id
        account = Account.objects.get(id = user)
        account.is_available = True
        detailedBook = DetailedBook.objects.get(detailed_id = bookId)
        detailedBook.detailed_returned = True
        book.loanedBook_statusId_id = 5
        book.loanedBook_dueDate = None
        book.loanedBook_startDate = None
        book.save()
        detailedBook.save()
        account.save()
    return HttpResponseRedirect(reverse('lendingPage'))
@login_required
def using(request,id):
    loanedBook = LoanedBook.objects.filter(loanedBook_receipt_id=id).only('loanedBook_statusId_id')
    for book in loanedBook:
        bookId = book.loanedBook_book_id
        receiptId = book.loanedBook_receipt_id
        getUser = Receipt.objects.get(receipt_id=receiptId)
        user = getUser.receipt_user_id
        account = Account.objects.get(id=user)
        account.is_available = False
        detailedBook = DetailedBook.objects.get(detailed_id=bookId)
        detailedBook.detailed_returned = False
        book.loanedBook_statusId_id = 6
        book.save()
        detailedBook.save()
        account.save()
    return HttpResponseRedirect(reverse('lendingPage'))
@login_required
def lendingAction(request):
    books = request.POST.getlist('bookInReceipts')
    admin = Account.objects.get(id=request.session['id'])
    failed = []
    for book in books:
        bookReceipt = LoanedBook.objects.get(loanedBook_id = book)
        bookN = bookReceipt.loanedBook_book_id
        bookNumber = str(bookN) #34
        # bookGet = Books.objects.get(book_id=bookNumber)
        detailedBook = DetailedBook.objects.get(detailed_id=bookNumber)
        bookId = detailedBook.detailed_book_id_id
        bookGet = Books.objects.get(book_id=bookId)
        currentPercent = detailedBook.detailed_book_percentage
        selected = request.POST['selectStatus' + book]
        percent = request.POST['condition'+book]
        price = bookGet.book_price
        diff = float(currentPercent) - float(percent)
        fee = float(price)*float(diff)/100
        currentFee = bookReceipt.loanedBook_fee
        if currentFee is None:
            finalFee = fee
        else:
            finalFee = currentFee + fee
        bookReceipt.loanedBook_statusId_id = selected
        today = datetime.datetime.today()
        receipt = bookReceipt.loanedBook_receipt_id
        receiptGet = Receipt.objects.get(receipt_id = receipt)
        userGet = receiptGet.receipt_user_id
        user = Account.objects.get(id = userGet)
        if selected == '7':
            bookReceipt.loanedBook_returnedDate = today
            bookReceipt.loanedBook_returnedStatus = percent
            bookReceipt.loanedBook_fee = finalFee
            bookReceipt.loanedBook_receive = admin
            user.is_available = True
            detailedBook.detailed_returned = True
            detailedBook.detailed_book_percentage = percent
        if selected == '3':
            detailedBook.detailed_retursned = False
            detailedBook.detailed_book_percentage = 0
            bookReceipt.loanedBook_returnedStatus = 0
            bookReceipt.loanedBook_fee = price
        user.save()
        detailedBook.save()
        bookReceipt.save()
    return HttpResponseRedirect(reverse('lendingPage'))

@login_required
def languageEdit(request,id):
    language = Language.objects.get(language_id = id)
    template = loader.get_template('language/edit.html')
    context = {
        'language': language
    }
    return HttpResponse(template.render(context, request))
@login_required
def languageUpdate(request,id):
    language = Language.objects.get(language_id=id)
    languageName = request.POST['language']
    code = request.POST['code']
    image = request.FILES.get('image')
    if image is None:
        language.language_name = languageName
        language.language_code = code
    else:
        language.language_name = languageName
        language.language_code = code
        language.language_image = image
    language.save()
    messages.success(request, (languageName + ' Updated Successfully !!!'))
    return HttpResponseRedirect(reverse('languageIndex'))
@login_required
def byLanguage(request,id):
    books = Books.objects.filter(book_language=id).prefetch_related()
    template = loader.get_template('language/books.html')
    context = {
        'books' : books
    }
    return HttpResponse(template.render(context,request))
@login_required
def detailedBook(request):
    detailedBooks = DetailedBook.objects.all()
    template = loader.get_template('detailed/index.html')
    context = {
        'detailedBooks': detailedBooks
    }
    return HttpResponse(template.render(context,request))
@login_required
def detailedBookAdd(request):
    books = Books.objects.all()
    template = loader.get_template('detailed/detailedBookAdd.html')
    context = {
        'books': books
    }
    return HttpResponse(template.render(context,request))
@login_required
def detailedBookUpdate(request):
    book = request.POST['book']
    percent = request.POST['percent']
    note = request.POST['note']
    amount = request.POST['amount']
    for a in range(int(amount)):
        detailedBook = DetailedBook(
            detailed_book_percentage = percent,
            detailed_book_id = Books.objects.get(book_id = book),
            detailed_book_note = note,
            detailed_importDate = datetime.date.today()
        )
        detailedBook.save()
    messages.success(request, ('Done!!!'))
    return HttpResponseRedirect(reverse('detailedBook'))
@login_required
def detailedBookEdit(request,id):
    percent = request.POST['percent']
    note = request.POST['note']
    detailed = DetailedBook.objects.get(detailed_id = id)
    detailed.detailed_book_percentage = percent
    detailed.detailed_book_note = note
    detailed.save()
    messages.success(request, ('Done!!!'))
    return HttpResponseRedirect(reverse('detailedBook'))
@login_required
def reload(request):
    sql = LoanedBook.objects.raw('SELECT * FROM book_loanedbook WHERE loanedBook_dueDate < DATE() AND loanedBook_statusId_id = 6')
    for x in sql:
        x.loanedBook_statusId_id = 2
        delta = datetime.date.today() - x.loanedBook_dueDate
        fee = 0.99 * delta.days
        x.loanedBook_fee = fee
        x.save()
    sql2 = LoanedBook.objects.raw('SELECT * FROM book_loanedbook WHERE loanedBook_statusId_id = 2')
    for y in sql2:
        delta = datetime.date.today() - y.loanedBook_dueDate
        fee = 0.99 * delta.days
        y.loanedBook_fee = fee
        y.save()
    return HttpResponseRedirect(reverse('lendingPage'))
@login_required
def detailedHistory(request,id):
    books = LoanedBook.objects.filter(loanedBook_book_id = id)
    template = loader.get_template('detailed/detailed_history.html')
    context = {
        'books': books
    }
    return HttpResponse(template.render(context, request))