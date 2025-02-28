from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Student, Staff, Course
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def register_student(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        gender = request.POST["gender"]
        course_id = request.POST["course"]
        email = request.POST["email"]
        phone = request.POST["phone"]

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")

        user = User.objects.create_user(username=username, password=password, email=email)
        course = Course.objects.get(id=course_id)  # Get selected course

        student = Student.objects.create(
            user=user, gender=gender, course=course, email=email, phone=phone
        )
        return HttpResponse("Registration successful. Wait for admin approval.")

    courses = Course.objects.all()  # Get all courses for dropdown
    return render(request, "register_student.html", {"courses": courses})

def login_student(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            student = Student.objects.filter(user=user).first()
            if student and student.is_approved:
                login(request, user)
                return redirect('student_dashboard')
            return render(request, 'login_student.html', {'error': 'Approval Pending or Rejected'})
        return render(request, 'login_student.html', {'error': 'Invalid Credentials'})
    return render(request, 'login_Student.html')

def register_staff(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        Staff.objects.create(user=user, is_approved=False)
        return redirect('login_staff')
    return render(request, 'register_staff.html')

def login_staff(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            staff = Staff.objects.filter(user=user).first()
            if staff and staff.is_approved:
                login(request, user)
                return redirect('staff_dashboard')
            return render(request, 'login_staff.html', {'error': 'Approval Pending or Rejected'})
        return render(request, 'login_staff.html', {'error' : 'Invalid Credentials'})
    return render(request, 'login_staff.html')

def logout_view(request):
    logout(request)
    return redirect(index)
    # return redirect('/')

def admin_dashboard(request):
    students = Student.objects.all()
    staff = Staff.objects.all()
    courses = Course.objects.all()
    return render(request, "admin_dashboard.html", {"students": students, "staff": staff, "courses": courses})

def student_dashboard(request):
    return render(request, 'student_dashboard.html')

def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

def approve_user(request, user_id, role):
    if role == "student":
        student = Student.objects.get(id=user_id)
        student.is_approved = True
        student.save()
    elif role == "staff":
        staff = Staff.objects.get(id=user_id)
        staff.is_approved = True
        staff.save()
    return redirect("admin_dashboard")

def reject_user(request, user_id, role):
    try:
        if role == "student":
            student = Student.objects.get(id=user_id)
            student.is_rejected = True
            student.save()
        elif role == "staff":
            staff = Staff.objects.get(id=user_id)
            staff.is_rejected = True
            staff.save()
    except Student.DoesNotExist or Staff.DoesNotExist:
        pass
    return redirect("admin_dashboard")


def add_course(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        Course.objects.create(name=name, description=description)
        return redirect("admin_dashboard")
    return render(request, "courses.html")

def available_courses(request):
    student = Student.objects.get(user=request.user)
    courses = Course.objects.all()
    registered_courses = StudentCourseRegistration.objects.filter(student=student).values_list("course_id", flat=True)
    return render(request, "available_courses.html", {"courses": courses, "registered_courses": registered_courses})