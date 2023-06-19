from django.contrib import admin

from gradebook_app.models import Semester, Course, Class, Lecturer, Student, Enrolment


admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Lecturer)
admin.site.register(Student)
admin.site.register(Enrolment)
