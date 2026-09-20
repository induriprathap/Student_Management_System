from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import students, Attendance, Marks
from .form import student_form, AttendanceForm, MarksForm

from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required


# ============================================================
# STUDENT DASHBOARD
# ============================================================

@login_required
def student_dashboard(request):

    # Superuser/Admin goes to Student Management
    if request.user.is_superuser:
        return redirect('std_lst')

    current_user = request.user

    try:
        # Find the student connected to the logged-in user
        student = students.objects.get(user=current_user)

        # Get marks
        marks = Marks.objects.filter(student=student)

        # ====================================================
        # ATTENDANCE
        # ====================================================

        present_count = Attendance.objects.filter(
            student=student,
            status="Present"
        ).count()

        absent_count = Attendance.objects.filter(
            student=student,
            status="Absent"
        ).count()

        total_attendance = present_count + absent_count

        if total_attendance > 0:
            attendance_percentage = (
                present_count / total_attendance
            ) * 100
        else:
            attendance_percentage = 0

        # ====================================================
        # MARKS ANALYTICS
        # ====================================================

        total_marks = sum(
            mark.marks_obtained
            for mark in marks
        )

        subject_count = marks.count()

        if subject_count > 0:

            average_marks = (
                total_marks / subject_count
            )

            highest_mark = max(
                mark.marks_obtained
                for mark in marks
            )

        else:

            average_marks = 0
            highest_mark = 0

    except students.DoesNotExist:

        return HttpResponse(
            "No student profile is linked to this user."
        )

    # ========================================================
    # DASHBOARD DATA
    # ========================================================

    context = {

        # Student
        'student': student,

        # Attendance
        'present': present_count,
        'absent': absent_count,
        'attendance_percentage': round(
            attendance_percentage,
            1
        ),

        # Marks
        'marks': marks,
        'total_marks': total_marks,
        'average_marks': round(
            average_marks,
            1
        ),
        'highest_mark': highest_mark,
        'subject_count': subject_count,
    }

    return render(
        request,
        'dashboard.html',
        context
    )


# ============================================================
# ADD ATTENDANCE
# ============================================================

@staff_member_required
def add_attendance(request, student_id):

    student = students.objects.get(
        id=student_id
    )

    if request.method == 'POST':

        form = AttendanceForm(
            request.POST
        )

        if form.is_valid():

            attendance = form.save(
                commit=False
            )

            attendance.student = student

            attendance.save()

            messages.success(
                request,
                'Attendance added successfully!'
            )

            return redirect(
                'std_lst'
            )

    else:

        form = AttendanceForm()

    return render(
        request,
        'add_attendance.html',
        {
            'form': form,
            'student': student
        }
    )


# ============================================================
# ADD MARKS
# ============================================================

@staff_member_required
def add_marks(request, student_id):

    student = students.objects.get(
        id=student_id
    )

    if request.method == 'POST':

        form = MarksForm(
            request.POST
        )

        if form.is_valid():

            mark = form.save(
                commit=False
            )

            mark.student = student

            mark.save()

            messages.success(
                request,
                'Marks added successfully!'
            )

            return redirect(
                'std_lst'
            )

    else:

        form = MarksForm()

    return render(
        request,
        'add_marks.html',
        {
            'form': form,
            'student': student
        }
    )


# ============================================================
# ADMIN CHECK
# ============================================================

def is_admin(user):

    return user.is_superuser


# ============================================================
# STUDENT LIST
# ============================================================

@login_required
def students_lst(request):

    query = request.GET.get(
        'search',
        ''
    )

    student_data = students.objects.all()

    # Search
    if query:

        student_data = student_data.filter(

            Q(name__icontains=query) |

            Q(roll__icontains=query) |

            Q(branch__icontains=query)

        )

    # Pagination
    paginator = Paginator(
        student_data,
        10
    )

    page = request.GET.get(
        'page'
    )

    student_data = paginator.get_page(
        page
    )

    return render(
        request,
        'students_list.html',
        {
            'students': student_data,
            'search_query': query
        }
    )


# ============================================================
# ADD STUDENT
# ============================================================

@user_passes_test(is_admin)
def add_student(request):

    if request.method == "POST":

        form = student_form(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Student Added Successfully!"
            )

            return redirect(
                "std_lst"
            )

        else:

            messages.error(
                request,
                "Form is invalid. Please check again."
            )

            return render(
                request,
                'student_form.html',
                {
                    'form': form,
                    'action': 'add_data'
                }
            )

    else:

        form = student_form()

        return render(
            request,
            "student_form.html",
            {
                'form': form,
                'action': 'add_data'
            }
        )


# ============================================================
# EDIT STUDENT
# ============================================================

def edit_student(request, id):

    student = get_object_or_404(
        students,
        id=id
    )

    if request.method == 'POST':

        form = student_form(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Student updated successfully!"
            )

            return redirect(
                "std_lst"
            )

    else:

        form = student_form(
            instance=student
        )

    return render(
        request,
        "student_form.html",
        {
            'form': form,
            'action': 'edit_data'
        }
    )


# ============================================================
# DELETE STUDENT
# ============================================================

def delete(request, id):

    student = get_object_or_404(
        students,
        id=id
    )

    student.delete()

    messages.success(
        request,
        "Student Deleted Successfully!"
    )

    return redirect(
        'std_lst'
    )


# ============================================================
# USER REGISTRATION
# ============================================================

def register_user(request):

    if request.method == "POST":

        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Registered successfully! Please login."
            )

            return redirect(
                'login'
            )

    else:

        form = UserCreationForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )