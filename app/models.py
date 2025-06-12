from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class CourseInstructor(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    institute = models.CharField(max_length=100)
    image = models.URLField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.name
    

semister_choice = (
    ('first-semester','first-semester'),
    ('second-semester','second-semester'),
    ('third-semester','third-semester'),
    ('fourth-semester','fourth-semester'),
    ('fifth-semester', 'fifth-semester'),
    ('sixth-semester','sixth-semester'),
    ('seventh-semester','seventh-semester'),
   
    
)

class Course(models.Model):
    name = models.CharField(max_length=100)
    picture = models.URLField(max_length=200, blank=True, null=True)
    description = models.TextField()
    start_date = models.DateField()
    price = models.IntegerField(default=0,null=True,blank=True)
    discount = models.IntegerField(default=0,null=True,blank=True)
    discounted_price = models.IntegerField(blank=True, null=True)
    end_date = models.DateField()
    enroll = models.BooleanField(default=False)
    semister = models.CharField(choices=semister_choice, max_length=20, blank=True, null=True)
    instructor = models.ForeignKey(CourseInstructor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
even_odd_choice = (
    ('Even',"Even"),
    ('Odd',"Odd"),
)
class Semsiter_Even_odd(models.Model):
    even_odd = models.CharField(choices=even_odd_choice,blank=True,null=True,max_length=10)

    def __str__(self):
        return self.even_odd

class Website_logo(models.Model):
    image = models.URLField()
    
class Slider_model(models.Model):
    image = models.URLField()
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tag_line = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title if self.title else "Slider Image"
    
    
class Class_video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video_url = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title if self.title else "Class Video"
    
class UserSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    
class CourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)
    expired_on = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.name}"
    
    
class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    device_type = models.CharField(max_length=20)
    os = models.CharField(max_length=50)
    browser = models.CharField(max_length=50)
    login_time = models.DateTimeField(auto_now_add=True)