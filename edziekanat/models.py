from django.db import models



class Institute(models.Model):
    name = models.CharField(max_length=70, unique=True)


class User(models.Model):
    email = models.CharField(max_length=70, unique=True)
    password = models.EmailField()

    class Meta:
        abstract = True


class Employee(User):
    role = models.CharField(max_length=10)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)


class Student(User):
    indexNumber = models.IntegerField(unique=True)


class Subject(models.Model):
    institution = models.ForeignKey(to=Institute, on_delete=models.CASCADE)
    name = models.CharField(max_length=70, unique=True)
    sem = models.IntegerField()
