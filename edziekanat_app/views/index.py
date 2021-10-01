import datetime

from django.db.models import Q, Count
from django.shortcuts import render

from edziekanat_app.models.tables.invoices.invoice import Invoice
from edziekanat_app.models.tables.invoices.invoice_category import InvoiceCategory
from edziekanat_app.models.tables.messages.message import Message
from edziekanat_app.models.tables.users.user import User


def index(request):
    average_time = get_average_decision_time()
    top_invoices = get_top_invoices()

    context = {
        'open_invoices': get_open_invoices(request.user),
        'closed_invoices': get_decision_invoices(request.user),
        'new_mesages': Message.objects.filter(reciever=request.user, seen=False),
        'all_invoices': get_user_invoices(request.user),
        'message': Message.objects.all(),
        'average_decision_time': average_time,
        'top_invoices': top_invoices
    }
    return render(request, 'index.html', context=context)


def get_open_invoices(user: User): return Invoice.objects.filter(status="W trakcie", created_by=user)


def get_decision_invoices(user: User): return Invoice.objects.filter(Q(status="Odrzucony") | Q(status="Zaakceptowany"),
                                                                     created_by=user, seen=False)


def get_user_invoices(user: User): return Invoice.objects.filter(created_by=user)


def format_timedelta(delta):
    days, rest = divmod(delta.total_seconds(), 86400)
    hours, rest = divmod(rest, 3600)
    minutes, seconds = divmod(rest, 60)
    return '{:01} dni {:01} h {:02} min'.format(int(days), int(hours), int(minutes))


def get_average_decision_time():
    invoices = Invoice.objects.all()
    if invoices.count() == 0:
        return 'brak podjętych decyzji'
    sum_time = datetime.timedelta()
    counter = 0
    for invoice in invoices:
        if invoice.decision_date is None:
            continue
        start = invoice.created_date.replace(tzinfo=None)
        end = invoice.decision_date.replace(tzinfo=None)
        sum_time += end - start
        counter += 1
    if counter == 0:
        return 'brak podjętych decyzji'

    return format_timedelta(sum_time / counter)


def get_top_invoices():
    invoices = Invoice.objects.all().values('category').annotate(total=Count('category')).order_by('total')
    top_five = []
    for invoice in invoices[:5]:
        top_five.append(InvoiceCategory.objects.filter(id=invoice['category']).first().name)
    return top_five
