from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion
from django.core.validators import MinValueValidator, MaxValueValidator


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SchoolClass",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="Class name")),
                (
                    "student",
                    models.ManyToManyField(
                        to=settings.AUTH_USER_MODEL,
                        limit_choices_to={"role": "STUDENT"},
                        related_name="classes",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="Subject name")),
            ],
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("topic", models.CharField(max_length=100, unique=True, verbose_name="Lesson topic")),
                ("homework", models.TextField(blank=True, verbose_name="Lesson topicHomework")),
                ("date", models.DateField(verbose_name="Date and time of the lesson")),
                (
                    "school_class",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to="journal.schoolclass",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to="journal.subject",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        limit_choices_to={"role": "TEACHER"},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Grade",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("grade", models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], verbose_name="Grade value")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="grades",
                        to="journal.lesson",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="grades",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("student", "lesson")},
            },
        ),
    ]
