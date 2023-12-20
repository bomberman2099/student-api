from django.db import models

class Student(models.Model):
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=128)