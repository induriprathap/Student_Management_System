"""
URL configuration for learning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from student import views as v
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("students/",v.students_lst,name="std_lst"),
    path('students/add/', v.add_student, name='add_student'),
    path('students/edit/<int:id>/', v.edit_student, name='edit_student'),
    path('students/delete/<int:id>/', v.delete, name='delete_student'),
    path("register/", v.register_user, name="register"),
    path("", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path('students/<int:student_id>/add-attendance/', v.add_attendance, name='add_attendance'),
    path('students/<int:student_id>/add-marks/', v.add_marks, name='add_marks'),  
    path('dashboard/', v.student_dashboard, name='dashboard'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
