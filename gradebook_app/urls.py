from django.urls import include, path
from rest_framework.routers import DefaultRouter

from gradebook_app import views
from gradebook_app.views import LecturerLoginView, StudentLoginView, UploadStudentView
from gradebook_app.viewsets import SemesterViewSet, CourseViewSet, LecturerViewSet, StudentViewSet, ClassViewSet, \
    EnrolmentViewSet

router = DefaultRouter()
router.register("semester", SemesterViewSet)
router.register("course", CourseViewSet)
router.register("lecturer", LecturerViewSet)
router.register("student", StudentViewSet)
router.register("class", ClassViewSet)
router.register("enrolment", EnrolmentViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('auth/lecturer/', LecturerLoginView, name='lecturer_login'),
    path('auth/student/', StudentLoginView, name='student_login'),

    path('manage-class-lecturer/<int:class_id>/', views.manage_class_lecturer, name='manage-class-lecturer'),
    path('manage-class-enrolment/<int:class_id>/', views.manage_class_enrolment, name='manage-class-enrolment'),
    path('enter_student_marks/', views.enter_student_marks, name='enter_student_marks'),
    path('view_student_marks/<int:student_id>/', views.view_student_marks, name='view_student_marks'),
    path('upload_students/', UploadStudentView, name='upload_students'),
]
