from django.shortcuts import render, redirect
from django.http import (HttpResponse, HttpResponseBadRequest, 
                         HttpResponseForbidden)

from .models import *
from django.contrib import messages
from django.core.mail import send_mail
import secrets
import string
import random
from django.conf import settings
from PatientApp.models import *
import ast  # Import ast for literal_eval
from PatientApp.views import *
# Create your views here.

def index(req):
    return render(req, 'index.html')

def Doctor_Registration(req):
    # DoctorRegistration.objects.all().delete()
    if req.method =="POST":
        name = req.POST['name']
        doctorid = req.POST['doctorid']
        hospital = req.POST['hospital']
        proffesion = req.POST['proffesion']
        email = req.POST['email']
        passcode = req.POST['passcode']
        confpasscode = req.POST['confpasscode']
        contact = req.POST['contact']
        address = req.POST['address']
        data = DoctorRegistration.objects.filter(doctorid=doctorid).exists()
        if data:
            msg = "This Doctor ID is already taken. Please choose another one."
            return render(req, 'Doctor_Registration.html', {'msg': msg})
        if DoctorRegistration.objects.filter(email=email).exists():
            msg= "This email address is already exists, try with another email"
            return render(req, 'Doctor_Registration.html', {'msg': msg})
        elif passcode != confpasscode:
            msg= "Password and confirm password does not match"
            return render(req, 'Doctor_Registration.html', {'msg': msg})
        doctor_data = DoctorRegistration(name=name,doctorid=doctorid,hospital=hospital,proffesion=proffesion, email=email, passcode=passcode, contact=contact, address=address)
        doctor_data.save()
        # Sending credentials through email
        email_subject = f'{name} Registration Successfull'
        email_message = f'Hello {name},\n\nThank you for registering with us!\n\nHere are your Login details:\n\nUser ID: {doctorid}\nPassword: {passcode}\n\nPlease keep this information safe.\n\nBest regards,\nYour Website Team'
        send_mail(email_subject, email_message, 'cse.takeoff@gmail.com', [email])
        update_password = DoctorRegistration.objects.get(email=email)
        update_password.passcode = passcode
        update_password.save()
        return render(req,'doctor_login.html',{'success': True} )
    
    return render(req, 'doctor_registration.html')

def Doctor_Login(request):
    if request.method == "POST":
        doctorid = request.POST.get('doctorid')
        passcode = request.POST.get('passcode')        
        try:
            doctor = DoctorRegistration.objects.get(doctorid=doctorid, passcode=passcode, status='active')
            
            if doctor.passcode == passcode:
                # Password matches, set the session
                request.session['doctorid'] = doctorid
                request.session['doctorname'] = doctor.name
                request.session['doctoremail'] = doctor.email
                return redirect('Doctorhome') 
            else:
                msg = "Invalid Doctor ID or Password"
                return render(request, 'doctor_login.html', {'msg': msg})

        except DoctorRegistration.DoesNotExist:
            msg = f"{doctorid} User Not Found Pls Register Or TA Not Accepted your request yet"
            return render(request, "Doctor_Login.html")
        
    return render(request, "Doctor_Login.html")

def Doctorhome(req):
    doctorname=req.session['doctorname']
    return render(req, 'Doctorhome.html', {'doctorname':doctorname})

def View_Patient_Requests(req):
    doctoremail= req.session['doctoremail']
    data = PatientUploadData.objects.filter(doctoremail=doctoremail, status="forwadedtodoctor")
    return render(req, 'View_Patient_Requests.html', {"data": data})

def PatientData(req, id):
    doctoremail= req.session['doctoremail']
    update_report = PatientUploadData.objects.get(id=id)

    patientname = update_report.patientname
    patientemail = update_report.patientemail
    patientfilename = update_report.filename

    encrypted_content = update_report.file.read()  # Read the content of the FieldFile
    key = update_report.key
    # Decrypt the content
    decrypted_content = aes_decrypt(key, encrypted_content)
    email_subject = f" {patientname} The patient, your report data securely viewed by the doctor, "
    email_message = f'Hello {patientemail},\n\n your {patientfilename} report data securely viewed by the doctor {doctoremail},!\n\nPlease keep this information safe.\n\nBest regards,\nYour Website Team'
    send_mail(email_subject, email_message, 'cse.takeoff@gmail.com', [patientemail])
    update_report.status = "reportgenerated"
    update_report.save()
    return render(req, 'PatientData.html', {"id": id, "decrypted_content": decrypted_content})

def keys_Patients(req, id):
    # Retrieve session data
    doctoremail = req.session.get('doctoremail')
    patientemail = req.session.get('patientemail')

    # Fetch data based on doctor and patient emails and status
    data = PatientUploadData.objects.filter(doctoremail=doctoremail, patientemail=patientemail, status="forwadedtodoctor")
    
    if data.exists():
        if req.method == "POST":
            # Retrieve form data as strings
            random_password = req.POST.get('key')
            # Convert form data to lists of integers or bytes
            # key = list(map(int, key_str.split(',')))

            # Filter data based on form inputs
            matchdata = PatientUploadData.objects.filter(
                doctoremail=doctoremail,
                patientemail=patientemail,
                random_password=random_password,
            )

            if matchdata.exists():
                return redirect('PatientData', id=id)
            else:
                msg = "Patient Data not Received To You Or Cloud Didn't Accepted yet patient request"
                return render(req, 'keys_Patients.html', {"id": id, "msg": msg, "data": data})

    # Render the initial form or data view
    return render(req, 'keys_Patients.html', {"id": id})
