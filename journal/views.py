from django.shortcuts import render

from django.http import HttpResponse

def lesson_list(request):
    return HttpResponse("<h1>List of lessons</h1>")

def lesson_detail(request, lesson_id):
    return HttpResponse(f"<h1>Details of lesson {lesson_id}</h1>")

def grade_list(request):
    return HttpResponse("<h1>List of grades</h1>")
