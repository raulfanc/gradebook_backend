from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# ==================Base Models==================
class Semester(models.Model):
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
    ]
    name = models.IntegerField(choices=SEMESTER_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    year = models.IntegerField(null=True, blank=True, editable=False)

    def generate_name(self):
        semester_choice = dict(self.SEMESTER_CHOICES)[self.name]
        return f'{semester_choice} {self.year}'

    def save(self, *args, **kwargs):
        self.year = self.start_date.year
        super().save(*args, **kwargs)

    def __str__(self):
        return self.generate_name()

    def get_absolute_url(self):
        return reverse('semester_detail', args=[str(self.id)])


class Course(models.Model):
    title = models.CharField(max_length=100)
    code = models.SlugField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    semesters = models.ManyToManyField(Semester, related_name='courses')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['code']


class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecturer_profile')
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    course = models.ManyToManyField(Course)
    DOB = models.DateField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        ordering = ['lastname', 'firstname']


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    DOB = models.DateField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        ordering = ['lastname', 'firstname']


class Class(models.Model):
    number = models.CharField(max_length=4, unique=True, default="", verbose_name='Class Code')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="classes")
    lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField(Student, through='Enrolment')

    def __str__(self):
        return f"{self.course} - {self.number}"

    class Meta:
        ordering = ['course', 'number']


# ==============end of Base Models=============


class Enrolment(models.Model):
    enrolled_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, db_column='studentID')
    enrolled_class = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='classID')
    enrollment_date = models.DateField(auto_now_add=True)
    grade_date = models.DateField(blank=True, null=True)
    grade = models.PositiveIntegerField(blank=True, null=True, verbose_name='Mark')

    class Meta:
        unique_together = ('enrolled_student', 'enrolled_class')

    def __str__(self):
        return f"{self.enrolled_student} - {self.enrolled_class}"
