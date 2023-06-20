from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Enrolment
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
    enrolments = Enrolment.objects.filter(enrolled_student_id=student_id)
    serializer = EnrolmentSerializer(enrolments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
