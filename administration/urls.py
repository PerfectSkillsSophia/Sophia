from django.urls import path
from administration.views import * 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    path('allAnswer/',allAnswer,name='allAnswer'),
    path('searchbar/',searchbar,name='searchbar'),
    path('generateresult/',generate_result,name='generate result'),
    path('addassessment/Add',Add_assessment,name='Add'),
    path('dashboard/assessment/<int:ass_id>/',view_assessments,name='view'),
    path('allAnswer/<int:ansId>/',view_analysis,name='view_analysis'),
    path('searchbar/allAnswer/<int:ansId>/',view_analysis,name='view_analysis'),
    path('administration/allAnswer/<int:ansId>/generate_transcript/', generate_tras, name='generate_transcript'),
    path('allAnswer/generate_tras/<int:ansId>/',generate_tras,name='generate_tras'),
    path('administration/tras/<int:ansId>/',generate_tras,name="tras"),
    path('searchbar/generate_tras/<int:ansId>/',generate_tras,name='generate_tras'),
    path('addquestion/',Add_question,name='Addquestion'),
    path('addassessment',add_assessment,name='addassessment'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)