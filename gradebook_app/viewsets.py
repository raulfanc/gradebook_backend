from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAdminUser

from gradebook_app.serializers import *
from gradebook_app.permissions import IsLecturer, IsStudent


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [IsAdminUser]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]


class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    permission_classes = [IsAdminUser]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAdminUser]


class EnrolmentViewSet(viewsets.ModelViewSet):
    queryset = Enrolment.objects.all()
    serializer_class = EnrolmentSerializer
    permission_classes = [IsLecturer, IsStudent, IsAdminUser]

    def get_permissions(self):
        if self.action in ['create', 'update', 'list', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsLecturer]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsStudent]
        return super().get_permissions()
