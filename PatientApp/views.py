from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
import secrets
import string
import random
from django.conf import settings
from DoctorApp.models import *
# Encryption and Decryption
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
from base64 import urlsafe_b64encode
from django.core.files.base import ContentFile
from django.core.files.base import ContentFile
from .utils import *
from django.contrib import messages

# Create your views here.
def generate_key():
    backend = default_backend()
    salt = os.urandom(16)
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=backend)
    key = kdf.derive(b"some_password")
    return key, salt

def encrypt_file(key, file_data):
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(file_data) + encryptor.finalize()
    return (ciphertext, iv, encryptor.tag)

def decrypt_file(key, iv, tag, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()




def Patient_Registration(req):
    # DoctorRegistration.objects.all().delete()
    if req.method =="POST":
        name = req.POST['name']
        patientid = req.POST['patientid']
        email = req.POST['email']
        passcode = req.POST['passcode']
        confpasscode = req.POST['confpasscode']
        contact = req.POST['contact']
        gender = req.POST['gender']
        age = req.POST['age']
        Aadhaar = req.POST['Aadhaar']
        # Check if patient ID already exists
        data = patientRegistration.objects.filter(patientid=patientid).exists()
        if data:
            msg = "This patient ID is already taken. Please choose another one."
            return render(req, 'patient_registration.html', {'msg': msg})
        if patientRegistration.objects.filter(email=email).exists():
            msg= "This email address is already exists, try with another email"
            return render(req, 'patient_registration.html', {'msg': msg})
        elif passcode != confpasscode:
            msg= "Password and confirm password does not match"
            return render(req, 'patient_registration.html', {'msg': msg})
        doctor_data = patientRegistration(
            name=name,
            patientid=patientid,
            email=email,
            passcode=passcode, 
            contact=contact, 
            gender=gender,
            age=age, 
            addar_card=Aadhaar
            )
        doctor_data.save()
        # Sending credentials through email
        email_subject = f'{name} Registration Successfull'
        email_message = f'Hello {name},\n\nThank you for registering with us!\n\nHere are your Login details:\n\nUser ID: {patientid}\nPassword: {passcode}\n\nPlease keep this information safe.\n\nBest regards,\nYour Website Team'
        send_mail(email_subject, email_message, 'cse.takeoff@gmail.com', [email])
        update_password = patientRegistration.objects.get(email=email)
        update_password.passcode = passcode
        update_password.save()
        return render(req,'patient_login.html',{'success': True} )
    
    return render(req, 'patient_registration.html')


def Patient_Login(request):
    # patientRegistration.objects.all().delete()
    if request.method == "POST":
        patientid = request.POST.get('patientid')
        passcode = request.POST.get('passcode')
    
        try:
            patient = patientRegistration.objects.get(patientid=patientid, passcode=passcode)
            
            if patient.passcode == passcode:
                # Password matches, set the session
                request.session['patientid'] = patientid
                request.session['patientname'] = patient.name
                request.session['patientemail'] = patient.email
                return redirect('Patienthome')
        
        except patientRegistration.DoesNotExist:
            msg = f"User with ID {patientid} not found. Please register first."
            return render(request, "patient_login.html", {'msg': msg})
        
    return render(request, "patient_login.html")

def Patienthome(req):
    patientname=req.session['patientname']
    return render(req, 'Patienthome.html', {'patientname':patientname})


def View_Doctors(req):
    # PatientUploadData.objects.all().delete()    
    patientname=req.session['patientname']
    doctor = DoctorRegistration.objects.all()

    return render(req, 'View_Doctors.html', {"doctor": doctor, 'patientname':patientname})



def Upload_Reports(req, id):
    # PatientUploadData.objects.all().delete()
    # Get all doctors to display in the form
    doctors = DoctorRegistration.objects.all()
    
    if req.method == "POST":
        try:
            # Get the selected doctor's email from the form submission
            doctoremail = req.POST['doctoremail']
            
        except KeyError:
            return render(req, 'Upload_Reports.html', {"id": id, "doctor": doctors, 'patientname': req.session['patientname'], 'error': "Doctor email is required."})

        patientid = req.session.get('patientid')
        patientemail = req.session.get('patientemail')
        patientname = req.session.get('patientname')
        filename = req.POST.get('filename')
        filedata = req.FILES.get('file')
        
        if not all([patientid, patientemail, patientname, filename, filedata]):
            return render(req, 'Upload_Reports.html', {"id": id, "doctor": doctors, 'patientname': req.session['patientname'], 'error': "All fields are required."})
        
        # Generate key and salt
        raw_key_bits = bb84_protocol_qiskit()
        shared_secret_key = generate_key_bytes(raw_key_bits)
        print("raw_key_bits", raw_key_bits)
        print("shared_secret_key", shared_secret_key)
        print('length of key is', len(shared_secret_key)) # Should be 16
        
        # Generating The random password (Unrelated to the fix, kept for context)
        length = 4
        characters = string.digits
        # Generate a random password
        random_password = ''.join(secrets.choice(characters) for _ in range(length))
        
        # Encrypt the file data
        # FIX: Use shared_secret_key (16 bytes) instead of raw_key_bits (list of 128 bits)
        encrypted_data = aes_encrypt(shared_secret_key, filedata.read())
        print('encrypted_data', encrypted_data)
        
        # Save encrypted file
        encrypted_file = ContentFile(encrypted_data, name=filename)
        
        # Create and save PatientUploadData instance
        upload = PatientUploadData(
            doctoremail=doctoremail,
            patientid=patientid, 
            patientemail=patientemail, 
            patientname=patientname,
            filename=filename,
            normalfiles=filedata,
            file=encrypted_file,
            key=shared_secret_key,
            random_password=random_password
        )
        upload.save()

        msg = f"{filename} file uploaded successfully "
        return render(req, 'Upload_Reports.html', {"id": id, "msg": msg, "doctor": doctors, 'success': True, 'patientname': patientname})
    
    return render(req, 'Upload_Reports.html', {"id": id, "doctor": doctors, 'patientname': req.session['patientname']})