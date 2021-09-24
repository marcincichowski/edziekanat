from django.db.models import *
from django.utils.translation import gettext as _


class Message(Model):
    sender = ForeignKey(to='edziekanat_app.User',
                        verbose_name=_('Nadawca'),
                        on_delete=CASCADE)

    reciever = ForeignKey(to='edziekanat_app.User',
                          verbose_name=_('Odbiorca'),
                          on_delete=CASCADE)

    message_text = CharField(_('Wiadomość'),
                             max_length=100)

    class Meta:
        db_table = "edziekanat_app_messages"
        verbose_name = "Wiadomość"
        verbose_name_plural = "Wiadomości"
