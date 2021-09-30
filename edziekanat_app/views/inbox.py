import datetime

from django.contrib import messages
from django.shortcuts import render, redirect

from ..forms import CreateMessage
from ..models.tables.messages.message import Message


def read_messages(request):
    messages = Message.objects.filter(reciever=request.user)
    for mess in messages:
        mess.seen = True
        mess.save()
    return redirect('/inbox')


def inbox(request):
    if request.method == 'POST':
        title = request.POST.get('message_title')
        text = request.POST.get('message_text')
        reciever = request.POST.get('reciever')
        if title is not None:
            if reciever == str(request.user.id):
                messages.warning(request, 'Nie możesz wysłać wiadomości do siebie.')
            else:
                try:
                    Message.objects.create(message_text=text,
                                           message_title=title,
                                           created_date=datetime.datetime.now(),
                                           reciever_id=reciever,
                                           sender_id=request.user.id).save()
                    messages.success(request, 'Wysłano wiadomość')
                except Exception as e:
                    messages.warning(request, f'Bład: {e.args[0]}')

    inbox_messages = Message.objects.filter(reciever=request.user).order_by('-created_date')
    return render(request, 'user/inbox.html', context={'inbox_messages': inbox_messages,
                                                       'new_message_form': CreateMessage()})
