# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password



class Student(AbstractUser):
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['password']
    USERNAME_FIELD = 'email'
    
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def _str_(self):
        return self.email
    
class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    instructor_name = models.CharField(max_length=100)
    prerequisites = models.CharField(max_length=100) 
    capacity = models.IntegerField(null=True)
    students = models.ManyToManyField(Student, through='Registration')  # Define many-to-many relationship


    def __str__(self):
        return f"{self.course_code} - {self.course_name}"
    
class CourseSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    days = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_no = models.CharField(max_length=50)  
    
    
    
class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Notification(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
from django.db.models import Count
from .models import Course, Registration

def enrollment_report():
    # Query the number of students enrolled in each course
    enrollment_data = Course.objects.annotate(num_enrolled=Count('students'))
    return enrollment_data

def popularity_report():
    # Query the popularity of courses based on enrollment numbers
    popularity_data = Course.objects.annotate(num_enrolled=Count('students')).order_by('-num_enrolled')
    return popularity_data
