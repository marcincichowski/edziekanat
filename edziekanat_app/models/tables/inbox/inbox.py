import json
from django.db.models import *
from django.utils.translation import gettext as _


class Inbox(Model):
    messages = CharField(max_length=10000)



    def set_Message(self, x):
        self.foo = json.dumps(x)

    def get_Message(self):
        return json.loads(self.messages)

    class Meta:
        db_table = "edziekanat_app_inboxes"
        verbose_name = "Skrzynka pocztowa"
        verbose_name_plural = "Skrzynki pocztowe"
