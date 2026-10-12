from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Q
from .models import Student
from .forms import StudentForm


@login_required
def dashboard(request):
    query = request.GET.get('q', '').strip()
    students = Student.objects.all().order_by('name')
    if query:
        students = students.filter(
            Q(name__icontains=query) | Q(email__icontains=query) | Q(course__icontains=query)
        )
    all_students = Student.objects.all()
    return render(request, 'students/dashboard.html', {
        'students': students,
        'total_students': all_students.count(),
        'courses_count': all_students.values('course').distinct().count(),
        'query': query,
        'username': request.user.username,
    })


@login_required
def add_student(request):
    form = StudentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student added successfully.')
        return redirect('dashboard')

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Add Student',
    })


@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student updated successfully.')
        return redirect('dashboard')

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Edit Student',
    })


@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        name = student.name
        student.delete()
        messages.success(request, f'{name} was removed.')
        return redirect('dashboard')

    return render(request, 'students/confirm_delete.html', {
        'student': student,
    })


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('dashboard')

