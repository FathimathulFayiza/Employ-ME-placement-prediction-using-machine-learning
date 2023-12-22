from django.db import models

# Create your models here.
class Student(models.Model):
    class Meta:
        db_table='Student'

    name = models.CharField(max_length=30,default=None)
    username = models.CharField(max_length=30,default=None)
    contact = models.CharField(max_length=30,default=None)
    email = models.CharField(max_length=50,default=None)
    age = models.CharField(max_length=30,default=None)
    address = models.CharField(max_length=250,default=None) 
    gender = models.CharField(max_length=10,default=None) 
    fatherName = models.CharField(max_length=50,default=None) 
    branch = models.CharField(max_length=250,default=None) 
    year = models.CharField(max_length=250,default=None) 
    Image = models.CharField(max_length=50,default=None) 
    Semister = models.CharField(max_length=50,default=None) 
    password = models.CharField(max_length=50,default=None) 
    is_register = models.IntegerField(default = 0)    
    is_enabled = models.IntegerField(default = 1)    


class Performance(models.Model):
    class Meta:
        db_table='Performance'
    
    Sslc = models.CharField(max_length=30,default=None) 
    StudentId = models.CharField(max_length=30,default=None)
    Puc = models.CharField(max_length=30,default=None)
    Be_cgpa = models.CharField(max_length=30,default=None)
    Deploma = models.CharField(max_length=50,default=None)
    Be_percentage = models.CharField(max_length=30,default=None)
    Backlog = models.CharField(max_length=50,default=None) 
    Cocubes_total = models.CharField(max_length=10,default=None) 
    Aptitude = models.CharField(max_length=50,default=None) 
    English = models.CharField(max_length=50,default=None) 
    Quantitative = models.CharField(max_length=50,default=None) 
    Compuer_fundamental = models.CharField(max_length=50,default=None) 
    Analytical = models.CharField(max_length=50,default=None) 
    Coding = models.CharField(max_length=50,default=None) 
    Domain = models.CharField(max_length=50,default=None) 
    Written_english = models.CharField(max_length=50,default=None) 
    Flag = models.IntegerField(default = 0)       


class PerformanceUpdate(models.Model):
    class Meta:
        db_table='PerformanceUpdate'
        
    Field = models.CharField(max_length=50,default=None)
    field_key = models.CharField(max_length=50,default=None)
    field_value = models.CharField(max_length=30,default=None)
    userId = models.IntegerField(default=None)
    flag = models.IntegerField(default = 0)
      