from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Lesson, Grade, SchoolClass
from .forms import LessonForm, GradeForm
from users.models import User


def get_user_model():
    teacher = User.objects.filter(role=User.Role.TEACHER).first()
    student = User.objects.filter(role=User.Role.STUDENT).first()
    return teacher, student


def teacher_lesson_list(request):
    teacher, _ = get_user_model()
    if not teacher:
        return HttpResponse("Please create at least one teacher in the admin panel.")

    lessons = Lesson.objects.filter(teacher=teacher).order_by('-date')
    return render(request, 'journal/teacher_lesson_list.html', {'lessons': lessons})


def teacher_lesson_create(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_lesson_list')
    else:
        form = LessonForm()
    return render(request, 'journal/teacher_lesson_form.html', {'form': form})


def lesson_detail(request, lesson_id):
    return HttpResponse(f"<h1>Details of lesson {lesson_id}</h1>")


def grade_list(request):
    return HttpResponse("<h1>List of grades</h1>")
