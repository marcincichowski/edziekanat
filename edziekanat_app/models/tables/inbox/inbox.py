import json
from django.db.models import *
from django.utils.translation import gettext as _


class Inbox(Model):
    messages = CharField(verbose_name=_('Lista wiadomości'),
                         max_length=10000)

    def set_message(self, x):
        self.foo = json.dumps(x)

    def get_message(self):
        return json.loads(self.messages)

    class Meta:
        db_table = "edziekanat_app_inboxes"
        verbose_name = "Skrzynka pocztowa"
        verbose_name_plural = "Skrzynki pocztowe"
