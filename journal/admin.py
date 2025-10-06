from django.contrib import admin

from django.contrib import admin
from .models import SchoolClass, Subject, Lesson, Grade

admin.site.register(SchoolClass)
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(Grade)