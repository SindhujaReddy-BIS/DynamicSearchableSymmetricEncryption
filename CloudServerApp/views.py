from django.shortcuts import render,redirect
from PatientApp.models import *
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
import secrets
import string
import random
from DoctorApp.models import *
# Create your views here.

def cloudserverlogin(request):
    if request.method=="POST":
        cloudserveremail = request.POST['cloudserveremail']
        cloudserverpassword = request.POST['cloudserverpassword']
        if cloudserveremail == "cloudserver@gmail.com" and cloudserverpassword =="cloudserver":
            request.session['cloudserveremail'] = cloudserveremail
            print(5555555555555555555)
            return render(request,'Cloud_home.html' ,{'success': True})
        else:
            # messages.add_message(request,messages.WARNING,"Invalid Credentials")
            return render(request,'cloudserverlogin.html')
    return render(request,"cloudserverlogin.html")

def Cloud_home(req):
    return render(req, 'Cloud_home.html')

def View_Requests(req):
    data = PatientUploadData.objects.all()
    return render(req, 'View_Requests.html', {"data": data})

def acceptrequest_patients(request, id):
    update = PatientUploadData.objects.get(id=id)
    update.status = "forwadedtodoctor"
    email = update.patientemail
    update.save()
    message = f'Hi {email},\n\nYour request has been securely forwarded to your doctor for review. You will be notified once your report is reviewed. Please do not reply to this email.\n\nThank you.\n\nRegards,\nAdmin'
    subject = "Dynamic Searchable Symmetric Encryption"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return redirect('View_Requests')

def reportcredentials(request, id):
    doctoremail = request.session['doctoremail']
    update = PatientUploadData.objects.filter(doctoremail=doctoremail, status="forwadedtodoctor")
    for data in update:
        patientid = data.patientid
        patientemail = data.patientemail 
        filename = data.filename
        key = data.key
        random = data.random_password
        email = data.doctoremail  # Correct assignment of email here
        data.save()  # Assuming you need to save the updated data back

        message = f'Hi {email},\n\nHere are patient email {patientemail} , and ID {patientid} of secure key details about the patient report file:\n\n Random_Password: {random} Key: {key}. Please do not reply to this email.\n\nThank you.\n\nRegards,\nAdmin'
        subject = "Report Security key details"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return redirect('View_Requests')



