from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class SchoolClass(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Class name")
    student = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='classes'
    )

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Subject name")

    def __str__(self):
        return self.name

class Lesson(models.Model):
    topic = models.CharField(max_length=100, unique=True, verbose_name="Lesson topic")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='lessons')
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    homework = models.TextField(blank=True, verbose_name="Lesson topicHomework")
    date = models.DateField(verbose_name="Date and time of the lesson")

    def __str__(self):
        return f"{self.topic} - {self.subject.name} ({self.date.strftime('%Y-%m-%d')})"

class Grade(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='grades')
    grade = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="Grade value"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student.username} - {self.lesson.topic}: {self.grade}"