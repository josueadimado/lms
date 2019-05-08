from django.db import models
from random import choice
from django.contrib.auth.models import AbstractUser
import django
from werkzeug.security import generate_password_hash
from datetime import datetime
from django.conf import settings

def numberOfDays(fromDate,toDate):
    from datetime import datetime
    date_format = "%m/%d/%Y"
    a = datetime.strptime(fromDate, date_format)
    b = datetime.strptime(toDate, date_format)
    delta = b - a
    return int(delta.days)

def numberOfWeeks(fromDate,toDate):
    return numberOfDays(fromDate,toDate)/7

def addDays(date,days):
    from datetime import timedelta
    from datetime import datetime
    date_format = "%m/%d/%Y"
    result = datetime.strptime(date, date_format) + timedelta(days=days)
    return result

class Department(models.Model):
    name = models.CharField(max_length=250,unique=True)
    short_name = models.CharField(max_length=25,null=True,blank=True)
    hod = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,on_delete=models.SET_NULL,related_name="emp_hod")
    dept_code = models.CharField(max_length=25,null=True,blank=True)
    date_created = models.DateTimeField(default=django.utils.timezone.now())

    def __str__(self):
        return self.name
    

# Create your models here.
COLOR_CHOICES = (('red','red'),('yellow','yellow'),('green','green'),('blue','blue'),('teal','teal'),('pink','pink'),('purple','purple'),)
class CustomUser(AbstractUser):
    # add additional fields in here
    email = models.EmailField(blank=False)
    is_staff = models.BooleanField( default=True)
    reg_joined = models.DateTimeField(default=django.utils.timezone.now())
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_activity = models.DateTimeField(default=django.utils.timezone.now())
    # user_img = models.ImageField(upload_to="accounts/uploads", null=True, blank=True)
    fav_color = models.CharField(max_length=10,choices=COLOR_CHOICES, default='blue')

import json 

all_countries = ( ('Ghana','Ghana'),('Togo','Togo'),('Ivory Coast','Ivory Coast') )
all_codes = (('GHA','233'),('TG','228'),('CID','225'))


genders = (('Male','Male'),('Female','Female'),('Other','Other'),('Rather not say','Rather not say'),)
STATUS = (('Married','Married'),('Single','Single'),('Other','Other'),('Rather not say','Rather not say'),)
CITY = (('Accra','Accra'),('Dodowa','Dodowa'),('Oyibi','Oyibi'),('Adenta','Adenta'),)
class Employee(CustomUser):
    email_token = models.CharField(max_length=1000,default=generate_password_hash(str(datetime.now())))
    email_confirmed = models.IntegerField(default=0)
    employee_id = models.CharField(max_length=200,null=True,blank=True) 
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,related_name="emp_dept",blank=True)
    date_of_birth = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=20,choices=genders, null=True,blank=True)
    marital_status = models.CharField(max_length=20,choices=STATUS, null=True,blank=True)
    city = models.CharField(max_length=20,choices=CITY, null=True,blank=True)
    country = models.CharField(max_length=20,choices=all_countries, default='Ghana')
    country_code = models.CharField(max_length=20,choices=all_codes, default='GHA')
    phone = models.CharField(max_length=9,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    
    class Meta:
        verbose_name = "Employee"

    def __str__(self):
        return self.username

class LeaveType(models.Model):
    leavetype = models.CharField(max_length=250,null=True,blank=True)
    creationDate = models.DateTimeField(null=True,default=django.utils.timezone.now())

    def __str__(self):
        return self.leavetype


STATUS = (('Approved','Approved'),('Pending','Pending'),('Disapproved','Disapproved'),)
class Leaves(models.Model):
    adminRemark = models.TextField(null=True,blank=True)
    adminRemarkDate = models.DateTimeField(null=True,default=django.utils.timezone.now())
    isRead = models.BooleanField(default=False)
    description = models.TextField(null=True,blank=True)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank = True, on_delete = models.SET_NULL)
    leavetype = models.ForeignKey(LeaveType, null=True,on_delete=models.SET_NULL,blank=True)
    fromDate = models.DateField(null=True,default=django.utils.timezone.now())
    postingDate = models.DateField(null=True,default=django.utils.timezone.now())
    toDate = models.DateField(null=True,default=django.utils.timezone.now())
    status = models.CharField(max_length=20,choices=STATUS, default='Pending')
    days = models.IntegerField(default=0)
    days_remaining = models.IntegerField(default=0)
    started = models.BooleanField(default=False)
    paused = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    date_approved = models.DateTimeField(null=True,default=django.utils.timezone.now())

    class Meta:
        verbose_name = "Leave"

    def __str__(self):
        myreturn = str(self.employee.username)+": "+ str(self.status)
        return myreturn

