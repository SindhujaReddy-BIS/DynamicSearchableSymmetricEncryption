from django.urls import path
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path("cloudserverlogin",cloudserverlogin , name="cloudserverlogin"),
    path("Cloud_home",Cloud_home , name="Cloud_home"),
    path("View_Requests",View_Requests , name="View_Requests"),
    path("reportcredentials/<int:id>/",reportcredentials , name="reportcredentials"),
    path("acceptrequest_patients/<int:id>/",acceptrequest_patients , name="acceptrequest_patients"),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)