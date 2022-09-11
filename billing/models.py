from operator import mod
from django.db import models
from django.contrib.postgres.fields import JSONField
# Create your models here.

class Customer_detail(models.Model):
    name=models.CharField(max_length=30)
    phoneno=models.PositiveBigIntegerField(unique=True)
    address=models.TextField(null=True,blank=True)
    email=models.EmailField(null=True,blank=True)

    def __str__(self):
        return self.name
    

class Sale(models.Model):
    bill_no=models.AutoField(primary_key=True)
    customer=models.ForeignKey(Customer_detail,on_delete=models.PROTECT)
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)
    vehicle_number=models.CharField(max_length=14,null=True,blank=True)
    orders=models.JSONField()
    total=models.PositiveIntegerField()
    discount=models.PositiveIntegerField()
    amount=models.PositiveIntegerField()
    def __str__(self):
        return "Bill No. : "+str(self.bill_no)

class Payment(models.Model):
    bill=models.OneToOneField(Sale,on_delete=models.PROTECT,primary_key=True)
    customer=models.ForeignKey(Customer_detail,on_delete=models.PROTECT)
    mode=models.CharField(max_length=20)
    gateway=models.CharField(max_length=20,null=True,blank=True)
    details=models.TextField(null=True,blank=True)
    pay_later_paid=models.PositiveIntegerField(null=True,blank=True)
    pay_later_balance=models.PositiveIntegerField(null=True,blank=True)
    remark=models.TextField(null=True,blank=True)

    def __str__(self):
        return "Bill : "+str(self.bill)

class Item(models.Model):
    iname=models.CharField(max_length=40,unique=True)
    iprice=models.DecimalField(max_digits=10,decimal_places=2)
    igst=models.DecimalField(max_digits=8,decimal_places=2)
    istock=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    isale=models.DecimalField(max_digits=16,decimal_places=2,null=True,blank=True,default=0)
    def __str__(self):
        return self.iname



    




