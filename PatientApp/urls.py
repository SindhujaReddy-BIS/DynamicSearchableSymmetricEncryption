from django.urls import path
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path("Patient_Registration/", Patient_Registration, name="Patient_Registration"),
    path("Patient_Login/", Patient_Login, name="Patient_Login"),
    path("Patienthome/", Patienthome, name="Patienthome"),
    path("View_Doctors/", View_Doctors, name="View_Doctors"),
    path('PatientApp/Upload_Reports/<int:id>/', Upload_Reports, name="Upload_Reports"),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)