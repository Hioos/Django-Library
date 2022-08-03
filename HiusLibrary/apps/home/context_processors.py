from apps.book.models import LoanedBook, Receipt


def nav_cats(request):
    if request.user.is_authenticated:
        pendings = Receipt.objects.raw('SELECT * FROM book_receipt INNER JOIN book_loanedbook ON receipt_id = loanedBook_receipt_id WHERE loanedBook_statusId_id =4  GROUP BY receipt_id ORDER BY receipt_timestamp DESC')
        count = Receipt.objects.raw('SELECT receipt_id,count(*) as countx FROM(SELECT * FROM book_receipt INNER JOIN book_loanedbook ON receipt_id = loanedBook_receipt_id WHERE loanedBook_statusId_id = 4 GROUP BY receipt_id)')
        return {
            'cppendings': pendings,
            'countPending' : count
        }
    return {}