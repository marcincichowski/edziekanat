from django.db.models import *
from django.utils.translation import gettext as _


class Message(Model):
    sender = ForeignKey(to='edziekanat_app.User',
                        verbose_name=_('Nadawca'),
                        on_delete=CASCADE, related_name="sender_user")

    reciever = ForeignKey(to='edziekanat_app.User',
                          verbose_name=_('Odbiorca'),
                          on_delete=CASCADE, related_name="reciever_user")

    message_text = CharField(_('Wiadomość'),
                             max_length=10)

    message_title = CharField(_('Tytuł'), max_length=15)

    created_date = DateTimeField(verbose_name=_('Data utworzenia'), auto_now=True)

    def __str__(self):
        return self.message_title

    class Meta:
        db_table = "edziekanat_app_messages"
        verbose_name = "Wiadomość"
        verbose_name_plural = "Wiadomości"
