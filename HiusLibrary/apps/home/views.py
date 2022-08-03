import datetime
from datetime import timedelta

from django.db.models import Sum, Q, Count
from django.db.models.functions import TruncDay
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from apps.accounts.models import Account
from apps.book.models import Receipt, LoanedBook, Language, Books


@login_required
def index(request):
    template = loader.get_template('home/index.html')
    books = Books.objects.raw(
        'SELECT * FROM book_books LEFT JOIN (SELECT loanedBook_book_id,count(*) as asd FROM book_loanedbook WHERE loanedBook_statusId_id = 2 OR loanedBook_statusId_id = 3 OR loanedBook_statusId_id = 6 GROUP BY loanedBook_book_id) ON loanedBook_book_id = book_id ORDER BY book_id DESC')
    receipts = Receipt.objects.all().order_by('-receipt_id')
    languages = Language.objects.all()
    chart2 = Language.objects.raw(
        'SELECT language_id,language_name,COUNT(book_language_id) as count  FROM book_language LEFT JOIN book_books ON book_language_id = language_id GROUP BY language_id ORDER BY count DESC')
    chart1 = LoanedBook.objects.raw(
        'SELECT loanedBook_id,book_loanedbook.loanedBook_statusId_id,loanStatus_name,COUNT(*) as count FROM book_loanedbook INNER JOIN loan_loanstatus ON loanedBook_statusId_id = loanStatus_id GROUP BY book_loanedbook.loanedBook_statusId_id ')
    sum = Books.objects.all().aggregate(set = Sum('book_amount'))
    count = LoanedBook.objects.filter(Q(loanedBook_statusId_id = 2)|Q(loanedBook_statusId_id = 3)|Q(loanedBook_statusId_id = 6)).count()
    items = Receipt.objects.filter(receipt_timestamp__lte=datetime.datetime.today(),
                               receipt_timestamp__gt=datetime.datetime.today() - datetime.timedelta(days=7)). \
        values('receipt_timestamp__date').annotate(count=Count('receipt_id'))
    users = Account.objects.filter(date_joined__lte=datetime.datetime.today(),
                                   date_joined__gt=datetime.datetime.today() - datetime.timedelta(days=7)). \
        values('date_joined__date').annotate(count=Count('id'))
    max = items.order_by('-count').first()
    min = items.order_by('count').first()
    context = {
        'receipts': receipts,
        'chart1': chart1,
        'languages': languages,
        'chart2': chart2,
        'count' : count,
        'items' : items,
        'sum' : sum,
        'max' : max,
        'min' : min,
        'users':users
    }
    return HttpResponse(template.render(context, request))
