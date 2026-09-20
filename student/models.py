from django.db import models
from django.contrib.auth.models import User

class students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=50)
    roll=models.IntegerField(unique=True)
    branch=models.CharField(max_length=10)
    email=models.EmailField()
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15,null=True, blank=True)
    address = models.TextField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name
    
class Attendance(models.Model):
    student = models.ForeignKey(students, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[("Present", "Present"), ("Absent", "Absent")])


class Marks(models.Model):
    student = models.ForeignKey(students, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks_obtained = models.IntegerField()
    



