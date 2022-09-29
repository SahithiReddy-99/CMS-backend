from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.core import validators
from django.db import models

from app.manager import UserManager
from app.views import validate_length

class Roles(models.Model):
    # roleId= models.AutoField(primary_key=True,auto_created=True)
    roleTypes = [
        ("Security", "Security"),
        ("Helper", "Helper"),
        ("Admin", "Admin"),
        ("Supervisor", "Supervisor"),
        ("User", "User"),
    ]
    role = models.CharField(choices=roleTypes, default="Helper", max_length=10)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.role



class User(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True,primary_key=True)
    firstName = models.CharField(max_length=15, null=True)
    lastName = models.CharField(max_length=15, null=True)
    password = models.CharField(max_length=30)
    mobileNo = models.CharField(max_length=10)
    confirm_password = models.CharField(max_length=30)
    occupation = models.CharField(max_length=30,blank=True, null=True)
    image = models.ImageField(upload_to='pictures', default=None, blank=True)
    isAdmin = models.BooleanField(default=False)
    address = models.CharField(max_length=50,blank=True, null=True)
    roleId = models.ForeignKey(Roles, on_delete=models.DO_NOTHING,null=True, blank=True)


    user_type_choice = (
        ('owner', 'owner'),
        ('staff', 'staff'),
    )
    user_type = models.CharField(choices=user_type_choice, default='customer', max_length=8)

    # # TODO: Added later
    session_token = models.CharField(max_length=10, default='0')

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    # def __str__(self):
    #     return self.firstName + ' ' + self.lastName + ' ' + self.user_type


class Block(models.Model):
    name= models.CharField(max_length=50)
    description = models.TextField()

class Flat(models.Model):
    flatNo= models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(max_length=50)
    # address = models.CharField(max_length=50)
    blockId = models.ForeignKey(Block, on_delete=models.DO_NOTHING,null=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True)


class Bill(models.Model):

    billTypes = [
        ("maintenance", "maintenance"),
        ("others", "others")
    ]
    type = models.CharField(choices=billTypes, default="electricity", max_length=20)
    date = models.DateField(auto_now=True)
    description = models.CharField(max_length=50)
    billNumber = models.IntegerField()
    # ownerId=models.ForeignKey(FlatOwner, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True)
    isPaid = models.BooleanField(default=False)
    totalBill = models.IntegerField()


class Reciept(models.Model):
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    billId = models.ForeignKey(Bill, on_delete=models.DO_NOTHING)
    paymentOptions = [
        ("UPI", "UPI"),
        ("Cash", "Cash"),
        ("Card", "Card"),
    ]
    paymentType = models.CharField(choices=paymentOptions, default="Cash", max_length=5)



# class Employees(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=50)
#     mobileNo = models.CharField(max_length=10)
#     email = models.EmailField(max_length=50, unique=True)
#     address = models.CharField(max_length=50)
#     roleId = models.ForeignKey(Roles, on_delete=models.DO_NOTHING)
#     password = models.CharField(max_length=15)
#     isAdmin = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.name
#

class Visitors(models.Model):
    flatId = models.ForeignKey(Flat, on_delete=models.DO_NOTHING)
    time = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class FlatServicedByEmployees(models.Model):
    employeeId = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    flatNo = models.ForeignKey(Flat, on_delete=models.DO_NOTHING)


class Reviews(models.Model):
    title=models.CharField(max_length=255,blank=True)
    reviews = models.TextField()
    email = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



