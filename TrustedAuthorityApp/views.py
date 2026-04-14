from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
import secrets
import string
import random
from DoctorApp.models import *
# Create your views here.



def TAlogin(request):
    if request.method=="POST":
        TAemail = request.POST['TAemail']
        TApassword = request.POST['TApassword']
        if TAemail == "TA@gmail.com" and TApassword =="TA":
            request.session['TAemail'] = TAemail
            print(5555555555555555555)
            return render(request,'TA_Home.html' ,{'success': True})
        else:
            # messages.add_message(request,messages.WARNING,"Invalid Credentials")
            return render(request,'TAlogin.html')
    return render(request,"TAlogin.html")

def TA_Home(req):
    return render(req, 'TA_Home.html')


def View_Doctor_Requests(req):
    data = DoctorRegistration.objects.filter(status="pending")
    return render(req, 'View_Doctor_Requests.html', {"data": data})

def acceptrequest(request, id):
    update = DoctorRegistration.objects.get(id=id)
    update.status = "active"
    email = update.email
    doctorid = update.doctorid
    passcode = update.passcode
    update.save()
    message = f'Hi {email},\n\nYour request has been securely accepted by the TA. You can login now using credentials securely \n\n ID:{doctorid} , \n\n Password:{passcode} . Please do not reply to this email.\n\nThank you.\n\nRegards,\nAdmin'
    subject = "Dynamic Searchable Symmetric Encryption"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return redirect('View_Doctor_Requests')
