from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from users.roles import TEACHERS_GROUP, STUDENT_GROUP
from .models import Lesson, Grade
from .forms import LessonForm, GradeForm
from users.models import User


def is_teacher(user):
    return user.groups.filter(name=TEACHERS_GROUP).exists()


def is_student(user):
    return user.groups.filter(name=STUDENT_GROUP).exists()


def get_user_model():
    teacher = User.objects.filter(role="TEACHER").first()
    student = User.objects.filter(role="STUDENT").first()
    return teacher, student


@login_required
@user_passes_test(is_teacher, login_url='/accounts/login/', redirect_field_name=None)
def teacher_lesson_list(request):
    teacher, _ = get_user_model()
    if not teacher:
        return HttpResponse("Please create at least one teacher in the admin panel.")

    lessons = Lesson.objects.filter(teacher=teacher).order_by('-date')
    return render(request, 'journal/teacher_lesson_list.html', {'lessons': lessons})


@login_required
@user_passes_test(is_teacher, login_url='/accounts/login/', redirect_field_name=None)
def teacher_lesson_create(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_lesson_list')
    else:
        form = LessonForm()
    return render(request, 'journal/teacher_lesson_form.html', {'form': form})


@login_required
@user_passes_test(is_teacher, login_url='/accounts/login/', redirect_field_name=None)
def teacher_lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    students = lesson.school_class.student.all()
    grades = {grade.student.id: grade for grade in lesson.grades.all()}

    student_grades = []
    for student in students:
        student_grades.append({
            'student': student,
            'grade': grades.get(student.id)
        })
    return render(request, 'journal/teacher_lesson_detail.html', {
        'lesson': lesson,
        'student_grades': student_grades
    })


@login_required
@user_passes_test(is_teacher, login_url='/accounts/login/', redirect_field_name=None)
def set_grade(request, lesson_id, student_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    student = get_object_or_404(User, id=student_id)

    grade_instance, created = Grade.objects.get_or_create(
        lesson=lesson,
        student=student,
        defaults={'grade': 1}
    )
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade_instance)
        if form.is_valid():
            form.save()
            return redirect('teacher_lesson_detail', lesson_id=lesson.id)
    else:
        form = GradeForm(instance=grade_instance)
    return render(request, 'journal/set_grade.html', {
        'form': form,
        'student': student,
        'lesson': lesson
    })


@login_required
@user_passes_test(is_student, login_url='/accounts/login/', redirect_field_name=None)
def student_lesson_list(request):
    _, student = get_user_model()
    if not student:
        return HttpResponse("Please create at least one student in the admin panel.")

    lessons = Lesson.objects.filter(school_class__student=student).distinct().order_by('-date')
    return render(request, 'journal/student_lesson_list.html', {'lessons': lessons})


@login_required
@user_passes_test(is_student, login_url='/accounts/login/', redirect_field_name=None)
def student_grade(request):
    _, student = get_user_model()
    if not student:
        return HttpResponse("Please create at least one student in the admin panel.")

    grades = Grade.objects.filter(student=student).select_related('lesson').order_by('-lesson__date')
    return render(request, 'journal/student_grade.html', {'grades': grades})


def grade_list(request):
    return student_grade(request)
