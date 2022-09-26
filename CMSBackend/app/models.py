from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.core import validators
from django.db import models

from app.manager import UserManager
from app.views import validate_length

class User(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True)
    firstName = models.CharField(max_length=15, null=True)
    lastName = models.CharField(max_length=15, null=True)
    password = models.CharField(max_length=30)
    username = models.CharField(max_length=10, unique=True)
    mobileNo= models.CharField(max_length=10)
    address = models.CharField(max_length=50)

    confirm_password = models.CharField(max_length=30)
    last_login = models.DateTimeField(null=True, blank=True,auto_now_add=True)


    # TODO: Added later
    session_token = models.CharField(max_length=10, default='0')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()



# class Block(models.Model):
#     id= models.IntegerField(primary_key=True)
#     name= models.CharField(max_length=50)
#     description = models.TextField()

class Flat(models.Model):
    id = models.IntegerField(primary_key=True)
    name= models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    # blockId = models.ForeignKey(Block, on_delete=models.DO_NOTHING)
    owner= models.ForeignKey(User,on_delete=models.DO_NOTHING)



class Bill(models.Model):
    id = models.IntegerField(primary_key=True,auto_created=True)
    billTypes=[
        ("water","water"),
        ("electricity","electricity"),
        ("maintenance","maintenance"),
        ("others","others")
    ]
    type = models.CharField(choices=billTypes,default="electricity",max_length=20)
    date= models.DateField(auto_now=True)
    description = models.CharField(max_length=50)
    billNumber=models.IntegerField()
    # ownerId=models.ForeignKey(FlatOwner, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    isPaid=models.BooleanField(default=False)
    totalBill= models.IntegerField()



class Reciept(models.Model):
    id= models.IntegerField(primary_key=True,auto_created=True)
    description = models.TextField()
    date= models.DateField(auto_now_add=True)
    billId= models.ForeignKey(Bill,on_delete=models.DO_NOTHING)
    paymentOptions=[
        ("UPI","UPI"),
         ("Cash","Cash"),
          ("Card","Card"),
    ]
    paymentType= models.CharField(choices=paymentOptions,default="Cash",max_length=5)



class Roles(models.Model):

    roleTypes={
        'security':'Security',
        'helper':'Helper',
        'admin':'Admin',
        'supervisor':'Supervisor'
    }
    id = models.CharField(choices=roleTypes,primary_key=True,default='helper')
    name= models.CharField(max_length=50)
    description = models.TextField()


class Employees(models.Model):
    id = models.IntegerField(primary_key=True)
    name= models.CharField(max_length=50)
    mobileNo = models.CharField(max_length=10)
    email = models.EmailField(max_length=50,unique=True)
    address= models.CharField(max_length=50)
    roleId= models.ForeignKey(Roles, on_delete=models.CASCADE,many=True)
    password = models.CharField(max_length=15)
    isAdmin = models.BooleanField(default=False)


class Visitors(models.Model):
    id = models.IntegerField(primary_key=True)
    flatId= models.ForeignKey(Flat, on_delete=models.DO_NOTHING)
    time= models.DateTimeField(auto_now_add=True)
    reason= models.CharField(max_length=50)
    name = models.CharField(max_length=50)


class FlatServicedByEmployees(models.Model):
    employeeId=models.ForeignKey(Employees,on_delete=models.DO_NOTHING)
    flatId = models.ForeignKey(Flat, on_delete=models.DO_NOTHING)


