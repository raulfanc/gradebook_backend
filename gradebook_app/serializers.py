from rest_framework import serializers
from .models import *


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    semesters = SemesterSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'code', 'description', 'semesters']


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['id', 'user', 'firstname', 'lastname', 'email', 'course', 'DOB']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'firstname', 'lastname', 'email', 'DOB']


class ClassSerializer(serializers.ModelSerializer):
    # display purpose only fields below:
    semester = SemesterSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    lecturer = LecturerSerializer(read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'number', 'semester', 'course', 'lecturer']


class EnrolmentSerializer(serializers.ModelSerializer):
    enrolled_student = StudentSerializer(read_only=True)
    enrolled_class = ClassSerializer(read_only=True)

    class Meta:
        model = Enrolment
        fields = ['id', 'enrolled_student', 'enrolled_class', 'enrollment_date', 'grade_date', 'grade']
