from django.urls import path
from . import views

urlpatterns = [
    path('lessons/', views.lesson_list, name='lesson-list'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson-detail'),
    path('grades/', views.grade_list, name='grade-list'),
]
