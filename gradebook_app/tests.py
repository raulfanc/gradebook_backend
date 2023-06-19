# tests.py
from django.test import TestCase
from django.contrib.auth.models import User

from .models import Semester, Course, Lecturer, Student, Class, Enrolment
from .serializers import SemesterSerializer, CourseSerializer, LecturerSerializer, StudentSerializer, ClassSerializer, \
    EnrolmentSerializer
import datetime


# checking if the Semester instance is correctly created.
class SemesterTestCase(TestCase):
    def setUp(self):
        self.semester_attributes = {
            'name': 1,
            'start_date': datetime.date(2023, 1, 1),
            'end_date': datetime.date(2023, 12, 31),
        }
        self.semester = Semester.objects.create(**self.semester_attributes)

    def test_semester_was_created(self):
        semester = Semester.objects.get(name=1)
        self.assertEqual(semester.start_date, self.semester_attributes['start_date'])
        self.assertEqual(semester.end_date, self.semester_attributes['end_date'])


# checking if the serializer correctly serializes a Semester instance.
class SemesterSerializerTestCase(TestCase):
    def setUp(self):
        self.semester_attributes = {
            'name': 1,
            'start_date': datetime.date(2023, 1, 1),
            'end_date': datetime.date(2023, 12, 31),
        }
        self.semester = Semester.objects.create(**self.semester_attributes)
        self.serializer = SemesterSerializer(instance=self.semester)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'start_date', 'end_date', 'year'])

    def test_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.semester_attributes['name'])
        self.assertEqual(data['start_date'], str(self.semester_attributes['start_date']))
        self.assertEqual(data['end_date'], str(self.semester_attributes['end_date']))
        self.assertEqual(data['year'], self.semester_attributes['start_date'].year)


# Checking if the Course instance is correctly created.
class CourseSerializerTestCase(TestCase):
    def setUp(self):
        self.semester_attributes = {
            'name': 1,
            'start_date': datetime.date(2023, 1, 1),
            'end_date': datetime.date(2023, 12, 31),
        }
        self.semester = Semester.objects.create(**self.semester_attributes)
        self.course_attributes = {
            'title': 'Test Course',
            'code': 'TC101',
            'description': 'Test course for unit testing',
        }
        self.course = Course.objects.create(**self.course_attributes)
        self.course.semesters.add(self.semester)
        self.serializer = CourseSerializer(instance=self.course)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'title', 'code', 'description', 'semesters'])

    def test_semesters_are_correct(self):
        """test if the CourseSerializer includes the semesters field"""
        data = self.serializer.data
        self.assertEqual(len(data['semesters']), 1)
        self.assertEqual(data['semesters'][0]['name'], self.semester_attributes['name'])
        self.assertEqual(data['semesters'][0]['start_date'], str(self.semester_attributes['start_date']))
        self.assertEqual(data['semesters'][0]['end_date'], str(self.semester_attributes['end_date']))
        self.assertEqual(data['semesters'][0]['year'], self.semester_attributes['start_date'].year)


class LecturerSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='huangbo', password='chishi')
        self.course_attributes = {
            'title': 'Test Course',
            'code': 'TC101',
            'description': 'Test course for unit testing',
        }
        self.course = Course.objects.create(**self.course_attributes)
        self.lecturer_attributes = {
            'user': self.user,
            'firstname': 'huang',
            'lastname': 'bo',
            'email': 'john.doe@example.com',
            'DOB': datetime.date(1980, 1, 1),
        }
        self.lecturer = Lecturer.objects.create(**self.lecturer_attributes)
        self.lecturer.course.add(self.course)
        self.serializer = LecturerSerializer(instance=self.lecturer)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'user', 'firstname', 'lastname', 'email', 'course', 'DOB'])

    def test_content(self):
        data = self.serializer.data
        self.assertEqual(data['user'], self.lecturer_attributes['user'].id)
        self.assertEqual(data['firstname'], self.lecturer_attributes['firstname'])
        self.assertEqual(data['lastname'], self.lecturer_attributes['lastname'])
        self.assertEqual(data['email'], self.lecturer_attributes['email'])
        self.assertEqual(data['DOB'], str(self.lecturer_attributes['DOB']))
        self.assertEqual(len(data['course']), 1)
        self.assertEqual(data['course'][0], self.course.id)


class StudentSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='testpass2')
        self.student_attributes = {
            'user': self.user,
            'firstname': 'Jane',
            'lastname': 'Doe',
            'email': 'jane.doe@example.com',
            'DOB': datetime.date(2000, 1, 1),
        }
        self.student = Student.objects.create(**self.student_attributes)
        self.serializer = StudentSerializer(instance=self.student)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'user', 'firstname', 'lastname', 'email', 'DOB'])

    def test_content(self):
        data = self.serializer.data
        self.assertEqual(data['user'], self.student_attributes['user'].id)
        self.assertEqual(data['firstname'], self.student_attributes['firstname'])
        self.assertEqual(data['lastname'], self.student_attributes['lastname'])
        self.assertEqual(data['email'], self.student_attributes['email'])
        self.assertEqual(data['DOB'], str(self.student_attributes['DOB']))
