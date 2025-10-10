from django import forms
from .models import Lesson, Grade

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['topic', 'subject', 'school_class', 'teacher', 'homework', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'lesson', 'grade']
        widgets = {
            'student': forms.HiddenInput(),
            'lesson': forms.HiddenInput(),
        }