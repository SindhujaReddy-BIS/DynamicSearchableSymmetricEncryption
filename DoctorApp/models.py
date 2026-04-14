from django.db import models

# Create your models here.


class DoctorRegistration(models.Model):
    name=models.CharField(max_length=100, null=True)
    doctorid = models.CharField(max_length=50,null=True)
    hospital = models.CharField(max_length=50,null=True)
    proffesion = models.CharField(max_length=50,null=True)
    email=models.EmailField(max_length=50,null=True)
    passcode= models.CharField(max_length=10)
    contact= models.CharField(max_length=100, null=True)
    address= models.CharField(max_length=100, null=True)
    status= models.CharField(max_length=20,default='pending')
    class Meta:
        db_table="DoctorRegistration"