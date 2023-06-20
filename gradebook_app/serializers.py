from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'start_date', 'end_date', 'year']


class CourseSerializer(serializers.ModelSerializer):
    semesters = SemesterSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'code', 'description', 'semesters']


class LecturerSerializer(serializers.ModelSerializer):
    user = UserSerializer(write_only=True)

    class Meta:
        model = Lecturer
        fields = ['id', 'user', 'firstname', 'lastname', 'email', 'course', 'DOB']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer(data=user_data)
        user.is_valid(raise_exception=True)
        user_instance = user.save()
        lecturer = Lecturer.objects.create(user=user_instance, **validated_data)
        return lecturer


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(write_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'firstname', 'lastname', 'email', 'DOB']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer(data=user_data)
        user.is_valid(raise_exception=True)
        user_instance = user.save()
        student = Student.objects.create(user=user_instance, **validated_data)
        return student


class ClassSerializer(serializers.ModelSerializer):
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
