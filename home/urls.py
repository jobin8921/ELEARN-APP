from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/staff/', views.register_staff, name='register_staff'),
    path('login/student/', views.login_student, name='login_student'),
    path('login/staff/', views.login_staff, name='login_staff'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/staff/', views.staff_dashboard, name='staff_dashboard'),
    path('approve/<int:user_id>/<str:role>/', views.approve_user, name='approve_user'),
    path('reject/<int:user_id>/<str:role>/', views.reject_user, name='reject_user'),
    path("add_course/", views.add_course, name="add_course"),
]
