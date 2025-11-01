from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='teacher_lesson_list', permanent=False)),
    path('lessons/', views.teacher_lesson_list, name='teacher_lesson_list'),
    path('lessons/new/', views.teacher_lesson_create, name='teacher_lesson_create'),
    path('lessons/<int:lesson_id>/', views.teacher_lesson_detail, name='teacher_lesson_detail'),
    path('lessons/<int:lesson_id>/students/<int:student_id>/grade/', views.set_grade, name='set_grade'),
    path('grades/', views.grade_list, name='grade_list'),
]
