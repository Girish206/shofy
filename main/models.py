from django.db import models


# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=200, null=True)
    email_id = models.CharField(max_length=200, primary_key=True)
    mobile_number = models.BigIntegerField(null=True)
    photo = models.ImageField(upload_to='users/', null=True)
    password = models.TextField()


class ShippingAddress(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    email_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    mobile_number = models.BigIntegerField(null=True)
    house_no = models.TextField(null=True)
    area = models.TextField(null=True)
    landmark = models.TextField(null=True)
    pincode = models.CharField(max_length=6, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    default_address = models.BooleanField(default=False)


class ContactUs(models.Model):
    id = models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=200, null=True)
    last_name=models.CharField(max_length=200, null=True)
    email_id = models.CharField(max_length=200, null=True)
    mobile_number = models.BigIntegerField(null=True)
    message=models.CharField(max_length=200, null=True)