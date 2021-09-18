from django.db import models

from edziekanat_app.models.institute import Institute


class Subject(models.Model):
    institution = models.ForeignKey(Institute, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    ects = models.IntegerField()
    sem = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['institution', 'name']
