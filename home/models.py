from django.db import models

from django.contrib.auth.models import User

# Model for Student
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

# Mode for Adding COurse
class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

# Model for Staff
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    
# Model for Admin dashboard
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)