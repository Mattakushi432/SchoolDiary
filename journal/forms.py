from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import Lesson, Grade
from users.roles import TEACHERS_GROUP, STUDENTS_GROUP

User = get_user_model()

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['topic', 'subject', 'school_class', 'teacher', 'homework', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            teachers_group = Group.objects.get(name=TEACHERS_GROUP)
            self.fields['teacher'].queryset = User.objects.filter(groups=teachers_group)
        except Group.DoesNotExist:
            self.fields['teacher'].queryset = User.objects.none()

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'lesson', 'grade']
        widgets = {
            'student': forms.HiddenInput(),
            'lesson': forms.HiddenInput(),
        }