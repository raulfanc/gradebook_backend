from django.contrib import admin

from gradebook_app.models import Semester, Course, Class, Lecturer, Student, Enrolment
# from gradebook_app.admin_config.enrolment_admin import EnrolmentAdmin
# from gradebook_app.admin_config.student_admin import StudentAdmin
# from gradebook_app.admin_config.class_admin import ClassAdmin
# from gradebook_app.admin_config.course_admin import CourseAdmin
# from gradebook_app.admin_config.lecturer_admin import LecturerAdmin
# from gradebook_app.admin_config.semester_admin import SemesterAdmin

# Register your models here.
# admin.site.register(Semester, SemesterAdmin)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(Class, ClassAdmin)
# admin.site.register(Lecturer, LecturerAdmin)
# admin.site.register(Student, StudentAdmin)
# admin.site.register(Enrolment, EnrolmentAdmin)

admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Lecturer)
admin.site.register(Student)
admin.site.register(Enrolment)
