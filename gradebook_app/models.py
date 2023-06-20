from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel
from model_utils import FieldTracker
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail

from gradebook_app_2 import settings


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


class Enrolment(TimeStampedModel):
    # TimeStampedModel is subclass of Django's Model class, so it has all the same methods and attributes
    enrolled_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True,
                                         db_column='studentID')
    enrolled_class = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='classID')
    enrollment_date = models.DateField(auto_now_add=True)
    grade_date = models.DateField(blank=True, null=True)
    grade = models.PositiveIntegerField(blank=True, null=True, verbose_name='Mark')

    class Meta:
        unique_together = ('enrolled_student', 'enrolled_class')

    def __str__(self):
        return f"{self.enrolled_student} - {self.enrolled_class}"

    tracker = FieldTracker()


# using signal to email grade to student when grade is updated
@receiver(post_save, sender=Enrolment)
def notify_student(sender, instance, **kwargs):
    if instance.tracker.has_changed('grade') and instance.grade is not None:
        student_email = instance.enrolled_student.email
        subject = "Your Grade is Available"
        message = f"Dear {instance.enrolled_student},\n\nYour grade for {instance.enrolled_class} is now available. Please log in to the Gradebook to view your grade.\n\nBest regards,\n{instance.enrolled_class.lecturer}\nLecturer"
        from_email = settings.DEFAULT_FROM_EMAIL  # Uses the default email in settings.py

        try:
            send_mail(subject, message, from_email, [student_email])
            print(f"Email sent to {instance.enrolled_student}.")
        except Exception as e:
            print(str(e))
