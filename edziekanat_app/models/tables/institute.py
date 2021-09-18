from django.db import models


class Institute(models.Model):
    name = models.CharField(max_length=70, unique=True)
    location = models.CharField(max_length=70)

    def __str__(self):
        return self.name
