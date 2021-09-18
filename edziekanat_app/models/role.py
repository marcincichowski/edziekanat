from django.db import models


class Role(models.Model):
    STUDENT = 1
    TEACHER = 2
    SECRETARY = 3
    SUPERVISOR = 4
    ADMIN = 5
    ROLE_CHOICES = (
        (STUDENT, 'student'),
        (TEACHER, 'teacher'),
        (SECRETARY, 'secretary'),
        (SUPERVISOR, 'supervisor'),
        (ADMIN, 'admin'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()
