from django.db import models

from django.contrib.auth.models import User

# Model for Adding Course
class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

# Model for Student
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

# Model for Staff
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)  # Single course assigned

    
# Model for Admin dashboard
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)