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

from apps.accounts.models import Account, PaymentHistory
from apps.book.models import Receipt, LoanedBook, Language, Books


@login_required
def index(request):
    today = datetime.date.today()
    end = today + datetime.timedelta(7)
    nearends = Account.objects.filter(is_admin=False, is_staff=False, is_superuser=False,expired_date__lte=end,expired_date__gte=today,is_banned=False)
    template = loader.get_template('home/index.html')
    books = Books.objects.raw(
        'SELECT * FROM book_books LEFT JOIN (SELECT loanedBook_book_id,count(*) as asd FROM book_loanedbook WHERE loanedBook_statusId_id = 2 OR loanedBook_statusId_id = 3 OR loanedBook_statusId_id = 6 GROUP BY loanedBook_book_id) ON loanedBook_book_id = book_id ORDER BY book_id DESC')
    receipts = Receipt.objects.all().order_by('-receipt_id')
    languages = Language.objects.all()
    chart2 = Language.objects.raw(
        'SELECT language_id,language_name,COUNT(book_language_id) as count  FROM book_language INNER JOIN book_books ON book_language_id = language_id GROUP BY language_id ORDER BY count DESC')
    chart1 = LoanedBook.objects.raw(
        'SELECT loanedBook_id,book_loanedbook.loanedBook_statusId_id,loanStatus_name,COUNT(*) as count FROM book_loanedbook INNER JOIN loan_loanstatus ON loanedBook_statusId_id = loanStatus_id GROUP BY book_loanedbook.loanedBook_statusId_id ')
    sum = Books.objects.all().aggregate(set = Sum('book_amount'))
    pending = Receipt.objects.raw(
        'SElECT receipt_id,COUNT(*) as countx FROM (SELECT * FROM book_receipt INNER JOIN book_loanedbook ON receipt_id = loanedBook_receipt_id WHERE loanedBook_statusId_id =4  GROUP BY receipt_id ORDER BY receipt_timestamp DESC)')
    count = LoanedBook.objects.filter(Q(loanedBook_statusId_id = 2)|Q(loanedBook_statusId_id = 3)|Q(loanedBook_statusId_id = 6)).count()
    items = Receipt.objects.filter(receipt_timestamp__lte=datetime.datetime.today(),
                               receipt_timestamp__gt=datetime.datetime.today() - datetime.timedelta(days=7)). \
        values('receipt_timestamp__date').annotate(count=Count('receipt_id'))
    users = Account.objects.filter(date_joined__lte=datetime.datetime.today(),
                                   date_joined__gt=datetime.datetime.today() - datetime.timedelta(days=7)). \
        values('date_joined__date').annotate(count=Count('id'))
    max = items.order_by('-count').first()
    min = items.order_by('count').first()
    last7days = PaymentHistory.objects.raw("SELECT history_Id,SUM(pricing_price) as price FROM (select * from accounts_paymenthistory LEFT JOIN accounts_pricing ON accounts_paymenthistory.pricing_id = accounts_pricing.pricing_id WHERE history_timestamp > (SELECT DATETIME('now', '-7 day')))")
    sumMoney = PaymentHistory.objects.raw('SELECT history_id,SUM(pricing_price) as moneys FROM accounts_paymenthistory INNER JOIN accounts_pricing ON accounts_paymenthistory.pricing_id = accounts_pricing.pricing_id')
    chart10 = PaymentHistory.objects.prefetch_related().filter(history_timestamp__lte = datetime.datetime.today(),history_timestamp__gt = datetime.datetime.today()-datetime.timedelta(days=7)).values('history_timestamp__date').order_by('history_timestamp__date').annotate(sum=Sum('pricing__pricing_price'))
    chart10min = chart10.order_by('sum').first()
    chart10max = chart10.order_by('-sum').first()
    context = {
        'nearends': nearends,
        'receipts': receipts,
        'chart1': chart1,
        'languages': languages,
        'chart2': chart2,
        'count' : count,
        'items' : items,
        'last7days': last7days,
        'sum' : sum,
        'max' : max,
        'sumMoney': sumMoney,
        'min' : min,
        'pending':pending,
        'users':users,
        'chart10':chart10,
        'chart10min':chart10min,
        'chart10max':chart10max
    }
    return HttpResponse(template.render(context, request))
