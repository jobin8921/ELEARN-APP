from django.db import models

from django.contrib.auth.models import User

# Model for Adding Course
class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Course price
    duration = models.CharField(max_length=50, default="") 

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

class Message(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Messages are course-specific
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Exam(models.Model):
    staff = models.ForeignKey("Staff", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateTimeField(null=True, blank=True) 
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(
        max_length=10, help_text="1, 2, 3, or 4 (Correct answer)"
    )

    def __str__(self):
        return self.question_text

# Student Exam Response
class ExamResponse(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=10, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.is_correct = self.selected_option == self.question.correct_option
        super().save(*args, **kwargs)

# Exam Results
class ExamResult(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    date_submitted = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    event_date=models.DateField()