from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from .models import SchoolClass, Subject, Lesson, Grade
from users.roles import TEACHERS_GROUP, STUDENTS_GROUP

User = get_user_model()


class JournalTestCase(TestCase):
    """Base test case with fixtures for journal app tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = Client()
        
        # Create groups
        self.teachers_group = Group.objects.create(name=TEACHERS_GROUP)
        self.students_group = Group.objects.create(name=STUDENTS_GROUP)
        
        # Create users
        self.teacher = User.objects.create_user(
            username='teacher1',
            email='teacher@test.com',
            password='testpass123'
        )
        self.teacher.groups.add(self.teachers_group)
        
        self.student1 = User.objects.create_user(
            username='student1',
            email='student1@test.com',
            password='testpass123'
        )
        self.student1.groups.add(self.students_group)
        
        self.student2 = User.objects.create_user(
            username='student2',
            email='student2@test.com',
            password='testpass123'
        )
        self.student2.groups.add(self.students_group)
        
        # Create school class
        self.school_class = SchoolClass.objects.create(name='Class 10A')
        self.school_class.student.add(self.student1, self.student2)
        
        # Create subject
        self.subject = Subject.objects.create(name='Mathematics')
        
        # Create lessons
        self.lesson1 = Lesson.objects.create(
            topic='Algebra Basics',
            subject=self.subject,
            school_class=self.school_class,
            teacher=self.teacher,
            homework='Complete exercises 1-10',
            date=date.today()
        )
        
        self.lesson2 = Lesson.objects.create(
            topic='Geometry Introduction',
            subject=self.subject,
            school_class=self.school_class,
            teacher=self.teacher,
            homework='Read chapter 5',
            date=date.today() - timedelta(days=1)
        )
        
        # Create grades
        self.grade1 = Grade.objects.create(
            student=self.student1,
            lesson=self.lesson1,
            grade=8
        )


class LessonListViewTests(JournalTestCase):
    """Tests for viewing the list of lessons"""
    
    def test_teacher_lesson_list_authenticated(self):
        """Test teacher can view their lesson list"""
        self.client.login(username='teacher1', password='testpass123')
        response = self.client.get(reverse('teacher_lesson_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Algebra Basics')
        self.assertContains(response, 'Geometry Introduction')
        self.assertEqual(len(response.context['lessons']), 2)
    
    def test_teacher_lesson_list_unauthenticated(self):
        """Test unauthenticated user is redirected to login"""
        response = self.client.get(reverse('teacher_lesson_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_student_cannot_access_teacher_lesson_list(self):
        """Test student cannot access teacher lesson list"""
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('teacher_lesson_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_lesson_list_ordering(self):
        """Test lessons are ordered by date (newest first)"""
        self.client.login(username='teacher1', password='testpass123')
        response = self.client.get(reverse('teacher_lesson_list'))
        
        lessons = response.context['lessons']
        self.assertEqual(lessons[0], self.lesson1)  # Today's lesson first
        self.assertEqual(lessons[1], self.lesson2)  # Yesterday's lesson second


class LessonCreateViewTests(JournalTestCase):
    """Tests for creating a new lesson"""
    
    def test_teacher_can_create_lesson(self):
        """Test teacher can create a new lesson"""
        self.client.login(username='teacher1', password='testpass123')
        
        lesson_data = {
            'topic': 'Trigonometry Basics',
            'subject': self.subject.id,
            'school_class': self.school_class.id,
            'teacher': self.teacher.id,
            'homework': 'Practice sine and cosine',
            'date': date.today() + timedelta(days=1)
        }
        
        response = self.client.post(reverse('teacher_lesson_create'), lesson_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('teacher_lesson_list'))
        
        # Verify lesson was created
        new_lesson = Lesson.objects.get(topic='Trigonometry Basics')
        self.assertEqual(new_lesson.teacher, self.teacher)
        self.assertEqual(new_lesson.subject, self.subject)
        self.assertEqual(new_lesson.school_class, self.school_class)
    
    def test_teacher_create_lesson_get_request(self):
        """Test GET request to lesson create view shows form"""
        self.client.login(username='teacher1', password='testpass123')
        response = self.client.get(reverse('teacher_lesson_create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
    
    def test_student_cannot_create_lesson(self):
        """Test student cannot access lesson creation"""
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('teacher_lesson_create'))
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_create_lesson_invalid_data(self):
        """Test creating lesson with invalid data"""
        self.client.login(username='teacher1', password='testpass123')
        
        invalid_data = {
            'topic': '',  # Empty topic
            'subject': self.subject.id,
            'school_class': self.school_class.id,
            'teacher': self.teacher.id,
            'date': 'invalid-date'
        }
        
        response = self.client.post(reverse('teacher_lesson_create'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Form redisplayed with errors
        
        # Verify lesson was not created
        self.assertFalse(Lesson.objects.filter(topic='').exists())


class GradeManagementTests(JournalTestCase):
    """Tests for adding and managing grades"""
    
    def test_teacher_can_set_grade(self):
        """Test teacher can set a grade for a student"""
        self.client.login(username='teacher1', password='testpass123')
        
        grade_data = {
            'student': self.student2.id,
            'lesson': self.lesson1.id,
            'grade': 9
        }
        
        response = self.client.post(
            reverse('set_grade', kwargs={
                'lesson_id': self.lesson1.id,
                'student_id': self.student2.id
            }),
            grade_data
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('teacher_lesson_detail', kwargs={'lesson_id': self.lesson1.id}))
        
        # Verify grade was created
        grade = Grade.objects.get(student=self.student2, lesson=self.lesson1)
        self.assertEqual(grade.grade, 9)
    
    def test_teacher_can_update_existing_grade(self):
        """Test teacher can update an existing grade"""
        self.client.login(username='teacher1', password='testpass123')
        
        # Update existing grade
        grade_data = {
            'student': self.student1.id,
            'lesson': self.lesson1.id,
            'grade': 10
        }
        
        response = self.client.post(
            reverse('set_grade', kwargs={
                'lesson_id': self.lesson1.id,
                'student_id': self.student1.id
            }),
            grade_data
        )
        
        self.assertEqual(response.status_code, 302)
        
        # Verify grade was updated
        updated_grade = Grade.objects.get(student=self.student1, lesson=self.lesson1)
        self.assertEqual(updated_grade.grade, 10)
    
    def test_set_grade_get_request(self):
        """Test GET request to set grade shows form"""
        self.client.login(username='teacher1', password='testpass123')
        
        response = self.client.get(
            reverse('set_grade', kwargs={
                'lesson_id': self.lesson1.id,
                'student_id': self.student1.id
            })
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertContains(response, self.student1.username)
        self.assertContains(response, self.lesson1.topic)
    
    def test_student_cannot_set_grade(self):
        """Test student cannot set grades"""
        self.client.login(username='student1', password='testpass123')
        
        response = self.client.get(
            reverse('set_grade', kwargs={
                'lesson_id': self.lesson1.id,
                'student_id': self.student1.id
            })
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_grade_validation(self):
        """Test grade validation (1-12 range)"""
        self.client.login(username='teacher1', password='testpass123')
        
        # Test invalid grade (too high)
        invalid_grade_data = {
            'student': self.student2.id,
            'lesson': self.lesson1.id,
            'grade': 15  # Invalid grade
        }
        
        response = self.client.post(
            reverse('set_grade', kwargs={
                'lesson_id': self.lesson1.id,
                'student_id': self.student2.id
            }),
            invalid_grade_data
        )
        
        # Should redisplay form with errors
        self.assertEqual(response.status_code, 200)
        
        # Verify invalid grade was not saved
        self.assertFalse(Grade.objects.filter(
            student=self.student2,
            lesson=self.lesson1,
            grade=15
        ).exists())


class LessonDetailViewTests(JournalTestCase):
    """Tests for lesson detail view"""
    
    def test_teacher_lesson_detail_view(self):
        """Test teacher can view lesson details with student grades"""
        self.client.login(username='teacher1', password='testpass123')
        
        response = self.client.get(
            reverse('teacher_lesson_detail', kwargs={'lesson_id': self.lesson1.id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.lesson1.topic)
        self.assertContains(response, self.student1.username)
        self.assertContains(response, self.student2.username)
        
        # Check student grades context
        student_grades = response.context['student_grades']
        self.assertEqual(len(student_grades), 2)
        
        # Verify grade is displayed for student1
        student1_data = next(sg for sg in student_grades if sg['student'] == self.student1)
        self.assertEqual(student1_data['grade'], self.grade1)
    
    def test_lesson_detail_nonexistent_lesson(self):
        """Test 404 for nonexistent lesson"""
        self.client.login(username='teacher1', password='testpass123')
        
        response = self.client.get(
            reverse('teacher_lesson_detail', kwargs={'lesson_id': 9999})
        )
        
        self.assertEqual(response.status_code, 404)


class StudentViewTests(JournalTestCase):
    """Tests for student-specific views"""
    
    def test_student_grade_list(self):
        """Test student can view their grades"""
        self.client.login(username='student1', password='testpass123')
        
        response = self.client.get(reverse('grade_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.grade1.grade))
        self.assertContains(response, self.lesson1.topic)


class IntegrationTests(JournalTestCase):
    """Integration tests for complete workflows"""
    
    def test_complete_lesson_workflow(self):
        """Test complete workflow: create lesson, add grades"""
        self.client.login(username='teacher1', password='testpass123')
        
        # 1. Create a new lesson
        lesson_data = {
            'topic': 'Integration Test Lesson',
            'subject': self.subject.id,
            'school_class': self.school_class.id,
            'teacher': self.teacher.id,
            'homework': 'Test homework',
            'date': date.today()
        }
        
        create_response = self.client.post(reverse('teacher_lesson_create'), lesson_data)
        self.assertEqual(create_response.status_code, 302)
        
        # Get the created lesson
        new_lesson = Lesson.objects.get(topic='Integration Test Lesson')
        
        # 2. View lesson list and verify it's there
        list_response = self.client.get(reverse('teacher_lesson_list'))
        self.assertContains(list_response, 'Integration Test Lesson')
        
        # 3. Add grades for students
        for student in [self.student1, self.student2]:
            grade_data = {
                'student': student.id,
                'lesson': new_lesson.id,
                'grade': 7
            }
            
            grade_response = self.client.post(
                reverse('set_grade', kwargs={
                    'lesson_id': new_lesson.id,
                    'student_id': student.id
                }),
                grade_data
            )
            self.assertEqual(grade_response.status_code, 302)
        
        # 4. Verify grades were created
        self.assertEqual(Grade.objects.filter(lesson=new_lesson).count(), 2)
        
        # 5. View lesson detail and verify grades are displayed
        detail_response = self.client.get(
            reverse('teacher_lesson_detail', kwargs={'lesson_id': new_lesson.id})
        )
        self.assertEqual(detail_response.status_code, 200)
        
        student_grades = detail_response.context['student_grades']
        for sg in student_grades:
            self.assertIsNotNone(sg['grade'])
            self.assertEqual(sg['grade'].grade, 7)
