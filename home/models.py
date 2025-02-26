from django.db import models

from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)