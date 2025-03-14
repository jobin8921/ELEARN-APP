from django.urls import path
from . import views

urlpatterns = [
    # home page
    path('', views.index, name='home'),
    # register and login for staff and student
    path('register/student/', views.register_student, name='register_student'),
    path('register/staff/', views.register_staff, name='register_staff'),
    path('login/student/', views.login_student, name='login_student'),
    path('login/staff/', views.login_staff, name='login_staff'),
    # url for logut button
    path('logout/', views.logout_view, name='logout'),
    # url for admin dashboard
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    # url for staff and student dashboard
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/staff/', views.staff_dashboard, name='staff_dashboard'),
    # url for approval and rejection of staff and student profile
    path('approve/<int:user_id>/<str:role>/', views.approve_user, name='approve_user'),
    path('reject/<int:user_id>/<str:role>/', views.reject_user, name='reject_user'),
    # adding course URL
    path("add_course/", views.add_course, name="add_course"),
    # view for the available courses
    path('courses_preview/', views.course_preview, name='course_preview'),


    path('upload-notes/', views.upload_notes, name='upload_notes'),

    # path('start-exam/<int:course_id>/', views.start_exam, name='start_exam'),

    path("students/", views.registered_students, name="registered_students"),

    path("delete_message/<int:message_id>/", views.delete_message, name="delete_message"),

]
