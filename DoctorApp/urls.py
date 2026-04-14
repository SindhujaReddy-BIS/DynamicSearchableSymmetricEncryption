from django.urls import path
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("Doctor_Registration/", Doctor_Registration, name="Doctor_Registration"),
    path("Doctor_Login/", Doctor_Login, name="Doctor_Login"),
    path("Doctorhome/", Doctorhome, name="Doctorhome"),
    path("View_Patient_Requests/", View_Patient_Requests, name="View_Patient_Requests"),
    path("keys_Patients/<int:id>/", keys_Patients, name="keys_Patients"),
    path("PatientData/<int:id>/", PatientData, name="PatientData"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)