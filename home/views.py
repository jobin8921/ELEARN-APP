from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Student, Staff, Course
from django.contrib import messages
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
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()  # Normalize username
        password = request.POST.get("password")
        name = request.POST.get("name")
        email = request.POST.get("email").strip().lower()
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")

        # Check if username exists (case-insensitive)
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
            return redirect("register_staff")

        # Check if email exists in Staff table
        if Staff.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email already exists. Please use another email.")
            return redirect("register_staff")

        # Create user
        user = User.objects.create_user(username=username, password=password, email=email)

        # Create staff profile (Pending approval)
        Staff.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone,
            gender=gender,
            is_approved=False,  # Staff needs admin approval
            is_rejected=False
        )

        messages.success(request, "Registration successful! Wait for admin approval before logging in.")
        return redirect("login_staff")

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
    # Fetch the staff profile, return None if not found
    staff = Staff.objects.filter(user=request.user).first()

    return render(request, 'staff_dashboard.html', {'staff': staff})

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

def assign_course(request):
    if request.method == "POST":
        staff_id = request.POST.get("staff_id")
        course_id = request.POST.get("course_id")

        print(f"Staff ID: {staff_id}, Course ID: {course_id}")  # ✅ Debugging Output

        # Ensure staff and course exist
        staff = get_object_or_404(Staff, id=staff_id)
        course = get_object_or_404(Course, id=course_id)

        # Assign the course
        staff.assigned_course = course
        staff.save()

        print(f"Assigned Course: {staff.assigned_course}")  # ✅ Debugging Output

        messages.success(request, f"Assigned '{course.name}' to {staff.name} successfully!")
        return redirect("admin_dashboard")  # ✅ Redirect after assignment

    staff = Staff.objects.filter(is_approved=True)  # ✅ Only approved staff
    courses = Course.objects.all()
    return render(request, "admin_dashboard.html", {"staff": staff, "courses": courses})