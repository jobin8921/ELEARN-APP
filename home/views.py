from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Student, Staff, Course, Message,Exam, Question, ExamResponse, ExamResult
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')

def register_student(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        name = request.POST["name"]
        gender = request.POST["gender"]
        course_id = request.POST["course"]
        email = request.POST["email"]
        phone = request.POST["phone"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register_student")

        user = User.objects.create_user(username=username, password=password, email=email)
        course = Course.objects.get(id=course_id)  # Get selected course

        Student.objects.create(
            user=user, name=name, gender=gender, course=course, email=email, phone=phone
        )

        messages.success(request, "Registration successful. Wait for admin approval.")
        return redirect("register_student")

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
    # Get the logged-in user
    user = request.user  

    try:
        # Fetch student details
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'Student profile not found'})

    # Get assigned staff
    exams = Exam.objects.filter(course=student.course)

    staff = Staff.objects.filter(course=student.course).first()



    # Get notifications for the student
    messages = Message.objects.filter(course=student.course).order_by("-created_at")

    # Pass student data to the template
    context = {
        'student': student,
        'staff': staff,
        'messages': messages,
        "exams": exams
        
    }
    
    return render(request, 'student_dashboard.html', context)

def staff_dashboard(request):
    # Fetch the staff member along with their assigned course
    staff = Staff.objects.filter(user=request.user).select_related("course").first()

    if not staff:
        return HttpResponse("Staff profile not found")

    # Fetch students who are assigned to the same course
    students = Student.objects.filter(course=staff.course)

    # Fetch messages related to the assigned course
    messages = Message.objects.filter(course=staff.course).order_by("-created_at")

    # Fetch uploaded notes
    # notes = Notes.objects.filter(course=staff.course).order_by("-uploaded_at")

    if request.method == "POST":
        message_content = request.POST.get("message_content", "").strip()  # Ensure it's not None
        
        if message_content:  # Check if it's not empty
            Message.objects.create(staff=staff, course=staff.course, content=message_content)
            return redirect("staff_dashboard")  
    
    return render(
        request, 
        "staff_dashboard.html", 
        {"staff": staff, "students": students, "messages": messages}
    )

def approve_user(request, user_id, role):
    if request.method == "POST":
        if role == "student":
            student = get_object_or_404(Student, id=user_id)
            student.is_approved = True
            student.is_rejected = False
            student.save()
            messages.success(request, f"{student.name} has been approved!")
        
        elif role == "staff":
            staff = get_object_or_404(Staff, id=user_id)
            selected_course_id = request.POST.get("course_id")  # Get selected course
            
            if selected_course_id:
                selected_course = get_object_or_404(Course, id=selected_course_id)
                staff.is_approved = True
                staff.course = selected_course  # Assign course
                staff.save()
                messages.success(request, f"{staff.name} has been approved and assigned to {selected_course.name}!")
            else:
                messages.error(request, "Please select a course before approving staff.")
                return redirect("admin_dashboard")

    return redirect("admin_dashboard")

def reject_user(request, user_id, role):
    try:
        if role == "student":
            student = get_object_or_404(Student, id=user_id)
            user = student.user  # Get the associated User
            student.delete()  # Delete student record
            user.delete()  # Delete user account
        elif role == "staff":
            staff = get_object_or_404(Staff, id=user_id)
            user = staff.user  # Get the associated User
            staff.delete()  # Delete staff record
            user.delete()  # Delete user account
    except Exception as e:
        print(f"Error: {e}")  # Log the error if needed
    
    return redirect("admin_dashboard")


def add_course(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        Course.objects.create(name=name, description=description)
        return redirect("admin_dashboard")
    return render(request, "add_courses.html")


def course_preview(request):
    return render(request, 'courses.html') 

def available_courses(request):
    student = Student.objects.get(user=request.user)
    courses = Course.objects.all()
    registered_courses = StudentCourseRegistration.objects.filter(student=student).values_list("course_id", flat=True)
    return render(request, "available_courses.html", {"courses": courses, "registered_courses": registered_courses})

def upload_notes(request):
    if request.method == "POST":
        course_id = request.POST.get("course")
        pdf_file = request.FILES.get("pdf_file")

        if course_id and pdf_file:
            course = Course.objects.get(id=course_id)
            Notes.objects.create(course=course, file=pdf_file)
            return HttpResponse("Notes uploaded successfully!")
        else:
            return HttpResponse("Please select a course and upload a file.")

    return redirect("staff_dashboard")  # Redirect after POST



@login_required
def registered_students(request):
    # Get the course assigned to the logged-in staff (assuming 'course' is a ForeignKey)
    staff_course = request.user.staff.course  # Ensure 'course' exists in Staff model
    
    # Fetch students enrolled in that specific course
    students = Student.objects.filter(course=staff_course)
    
    return render(request, "students_list.html", {"students": students})

def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.staff.user == request.user:
        message.delete()

    return redirect("staff_dashboard")

def create_exam(request):
    staff = get_object_or_404(Staff, user=request.user)

    if request.method == "POST":
        title = request.POST["title"]
        date = request.POST["date"]
        duration = request.POST["duration"]

        exam = Exam.objects.create(
            staff=staff, course=staff.course, title=title, date=date, duration=duration
        )
        return redirect("add_question", exam_id=exam.id)

    return render(request, "create_exam.html", {"staff": staff})

@login_required
def add_question(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id, staff__user=request.user)

    if request.method == "POST":
        question_text = request.POST["question_text"]
        option1 = request.POST["option1"]
        option2 = request.POST["option2"]
        option3 = request.POST["option3"]
        option4 = request.POST["option4"]
        correct_option = request.POST["correct_option"]

        Question.objects.create(
            exam=exam,
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
        )
        return redirect("staff_dashboard")

    return render(request, "add_question.html", {"exam": exam})


@login_required
def take_exam(request, exam_id):
    student = get_object_or_404(Student, user=request.user)
    exam = get_object_or_404(Exam, id=exam_id, course=student.course)
    questions = exam.questions.all()  # Fetch all related questions

    if request.method == "POST":
        score = 0
        total_questions = questions.count()

        for question in questions:
            selected_option = request.POST.get(f"question_{question.id}", None)

            if selected_option:
                # Avoid duplicate responses
                ExamResponse.objects.update_or_create(
                    student=student, exam=exam, question=question,
                    defaults={"selected_option": selected_option}
                )

                if selected_option == question.correct_option:
                    score += 1

        # Save exam result
        ExamResult.objects.update_or_create(
            student=student, exam=exam,
            defaults={"score": score, "total_questions": total_questions}
        )

        return redirect("view_exam_results", exam_id=exam.id,)


    return render(request, "take_exam.html", {"exam": exam, "questions": questions})


@login_required
def view_exam_results(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)  # Ensure exam exists

    # If the user is a student, check if they are enrolled in this exam's course
    if hasattr(request.user, "student"):  
        student = request.user.student  # Get logged-in student
        if student.course != exam.course:
            return HttpResponse("You are not enrolled in this exam.", status=403)

        # Fetch only this student's results
        results = ExamResult.objects.filter(exam=exam, student=student)
    else:
        # If the user is a staff member, show all student results
        results = ExamResult.objects.filter(exam=exam)

    return render(request, "view_exam_results.html", {"exam": exam, "results": results})
