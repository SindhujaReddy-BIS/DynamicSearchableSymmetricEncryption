from django.urls import path
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path("TAlogin/", TAlogin, name="TAlogin"),
    path("TA_Home/", TA_Home, name="TA_Home"),
    path("View_Doctor_Requests/", View_Doctor_Requests, name="View_Doctor_Requests"),
    path("acceptrequest/<int:id>/", acceptrequest, name="acceptrequest"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)