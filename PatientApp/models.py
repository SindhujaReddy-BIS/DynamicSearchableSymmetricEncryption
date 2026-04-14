from django.db import models

# Create your models here.
class patientRegistration(models.Model):
    name=models.CharField(max_length=100, null=True)
    patientid = models.CharField(max_length=50,null=True)
    passcode= models.CharField(max_length=10)    
    email=models.EmailField(max_length=50,null=True)
    contact= models.CharField(max_length=100, null=True)
    gender= models.CharField(max_length=100, null=True)
    age= models.CharField(max_length=100, null=True)
    addar_card = models.CharField(max_length=20, null=True)
    class Meta:
        db_table="patientRegistration"

class PatientUploadData(models.Model):
    doctoremail= models.CharField(max_length=50, null=True)
    patientid = models.CharField(max_length=50)
    patientemail = models.EmailField()
    patientname = models.CharField(max_length=100)
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to="encrypted_patientfiles/%y", null=True)
    normalfiles = models.FileField(upload_to="normalfiles/%y", null=True)
    encryption_key = models.BinaryField()
    status= models.CharField(max_length=50, default= "pending", null=True)
    # Fields for encryption
    key = models.BinaryField(null=True)  # Store key as binary data
    random_password = models.CharField(max_length=255,null=True)
    class Meta:
        db_table = "PatientUploadData"

class payment_model(models.Model):
    useremail = models.EmailField(null=True)
    card_number = models.CharField(max_length=50, null=True)
    amount = models.CharField(max_length=10, null=True)
    expery_date = models.CharField(max_length=50, null=True)
    cvv = models.CharField(max_length=10, null=True)
    doctoremail = models.EmailField(null=True)

    class Meta:
        db_table = 'payment_model'