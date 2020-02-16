from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from datetime import datetime



class scanupload(models.Model):
    CHOICES = (
        ('allow', 'Allow'),
        ('pending', 'Pending'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    upload_Main_Img = models.ImageField( blank=True, null=True)
    visiname = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    status =  models.CharField(max_length=50, choices= CHOICES, blank=True, default = "pending")








class friendvisitor(models.Model):
    CHOICES = (
            ('allow', 'Allow'),
            ('pending', 'Pending'),
        )
    Pay_CHOICES = (
                ('paid', 'paid'),
                ('not paid', 'not paid'),
            )
    Response_CHOICES = (
                    ('not collected', 'not collected'),
                    ('collected', 'collected'),
                )
    Bag_CHOICES = (
   ('Bag', 'Bag'),
   ('Bin', 'Bin'),
   ('Other', 'Other')
)

    Area_CHOICES = (
   ('Area A', 'Area A'),
   ('Area B', 'Area B'),
   ('Area C', 'Area C')
)
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=10, blank=True, null=True, default="5756798953")
    Location = models.CharField(max_length=50, blank=True, null=True, choices = Area_CHOICES)
    Type = models.CharField(max_length=50,blank=True, null=True,choices=Bag_CHOICES)
    unit = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, to_field="username", on_delete=models.PROTECT, default="vijay")
    date = models.DateTimeField(default=datetime.now, blank=True)
    status =  models.CharField(max_length=50, choices= CHOICES, blank=True, default = "pending")
    reward =  models.CharField(max_length=50, choices= Pay_CHOICES, blank=True, default = "not paid")
    response =  models.CharField(max_length=50, choices= Response_CHOICES, blank=True, default = "not collected")





class urgentvisitor(models.Model):
    CHOICES = (
            ('allow', 'Allow'),
            ('pending', 'Pending'),
        )
    Bag_CHOICES = (
   ('Bag', 'Bag'),
   ('Bin', 'Bin'),
   ('Other', 'Other')
)

    Area_CHOICES = (
   ('Area A', 'Area A'),
   ('Area B', 'Area B'),
   ('Area C', 'Area C')
)
    Pay_CHOICES = (
                ('paid', 'paid'),
                ('not paid', 'not paid'),
            )
    Response_CHOICES = (
                    ('not collected', 'not collected'),
                    ('collected', 'collected'),)
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=10, blank=True, null=True, default="5756798953")
    Location = models.CharField(max_length=50, blank=True, null=True, choices = Area_CHOICES)
    Type = models.CharField(max_length=50,blank=True, null=True,choices=Bag_CHOICES)
    unit = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, to_field="username", on_delete=models.PROTECT, default="vijay")
    date = models.DateTimeField(default=datetime.now, blank=True)
    status =  models.CharField(max_length=50, choices= CHOICES, blank=True, default = "pending")
    reward =  models.CharField(max_length=50, choices= Pay_CHOICES, blank=True, default = "not paid")
    response =  models.CharField(max_length=50, choices= Response_CHOICES, blank=True, default = "not collected")
