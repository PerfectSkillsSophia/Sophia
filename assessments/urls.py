from django.urls import path
from assessments.views import * 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('welcome/<slug:ass_name>/',welcomeScreen,name='welcome'),
    path('feedback/',feedback,name='feedback'),
    path('answer/',answer,name='answer'),
    path('answer/fileUpload/',fileUpload, name='fileUpload'),
    path('thankyou/',thankyou, name='thankyou'),
    path('afterlogin/',afterlogin,name='afterlogin'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
