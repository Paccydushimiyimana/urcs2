from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    image = models.ImageField(upload_to='profiles/',default='avatar.png')
    phone = models.CharField(max_length=20, null=True)
    category = models.CharField(max_length=100, null=True)
    student = models.CharField(max_length=100, null=True)
    regNo=models.CharField(max_length=9, null=True)
    lecturer = models.CharField(max_length=100, null=True)
    staffId=models.CharField(max_length=9, null=True)
    college_council = models.CharField(max_length=100, null=True)
    academic_council = models.CharField(max_length=100, null=True)
    school_council=models.CharField(max_length=100, null=True)
    department_council=models.CharField(max_length=100, null=True)
    school=models.CharField(max_length=100, null=True)
    department=models.CharField(max_length=100, null=True)
    level=models.CharField(max_length=5, null=True)
    unreads=models.PositiveIntegerField(default=0)
    
class Category(models.Model):
    name=models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Student_category(models.Model):
    name=models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Lecturer_category(models.Model): 
    name=models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name       

class College_council(models.Model):
    name=models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class School_council(models.Model):
    name=models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Department_council(models.Model):
    name=models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name       

class Academic_council(models.Model):
    name=models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name 

class College(models.Model):
    name=models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class School(models.Model):
    name=models.CharField(max_length=100, unique=True)
    college=models.ForeignKey(College, related_name='schools', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name=models.CharField(max_length=100, unique=True)
    levels=models.PositiveIntegerField(default=4)
    school=models.ForeignKey(School, related_name='departments',on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    

