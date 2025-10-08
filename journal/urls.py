from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Redirect the site root to the lessons list as a simple home page
    path('', RedirectView.as_view(pattern_name='lesson-list', permanent=False)),
    path('lessons/', views.lesson_list, name='lesson-list'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson-detail'),
    path('grades/', views.grade_list, name='grade-list'),
]
