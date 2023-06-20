import pandas as pd
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import Enrolment, Student, Lecturer
from .permissions import IsLecturer, IsStudent
from .serializers import EnrolmentSerializer


@api_view(['POST'])
@permission_classes([IsLecturer | IsAdminUser])
def enter_student_marks(request):
    enrolment_id = request.data.get('enrolment_id')
    grade = request.data.get('grade')

    try:
        enrolment = Enrolment.objects.get(id=enrolment_id)
        enrolment.grade = grade
        enrolment.save()
        serializer = EnrolmentSerializer(enrolment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Enrolment.DoesNotExist:
        return Response({'error': 'Enrolment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsLecturer | IsStudent | IsAdminUser])
def view_student_marks(request, student_id):
    if request.user.groups.filter(name="student").exists() and student_id != request.user.student_profile.id:
        return Response({'error': 'You are not authorized to view marks for this student.'},
                        status=status.HTTP_403_FORBIDDEN)

    enrolments = Enrolment.objects.filter(enrolled_student_id=student_id)
    serializer = EnrolmentSerializer(enrolments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class LecturerLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.groups.filter(name="lecturer").exists():
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


LecturerLoginView = LecturerLoginView.as_view()


class StudentLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.groups.filter(name="student").exists():
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


StudentLoginView = StudentLoginView.as_view()


class UploadStudentView(APIView):
    parser_class = (FileUploadParser,)
    permission_classes = [IsAdminUser]  # Only allow admin users to access this view

    def post(self, request, *args, **kwargs):

        file = request.data['file']
        data = pd.read_excel(file)

        for index, item in data.iterrows():
            first_name = item['firstname']
            last_name = item['lastname']
            username = item['username']
            email = item['email']
            dob = item['dob']
            group_name = item['group'].lower()

            if User.objects.filter(username=username).exists():
                continue

            default_password = '123'
            user = User.objects.create_user(username, email, default_password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if group_name == 'student':
                Student.objects.create(user=user, firstname=first_name, lastname=last_name, email=email, DOB=dob)
            elif group_name == 'lecturer':
                Lecturer.objects.create(user=user, firstname=first_name, lastname=last_name, email=email, DOB=dob)

        return Response(status=status.HTTP_201_CREATED)


UploadStudentView = UploadStudentView.as_view()
