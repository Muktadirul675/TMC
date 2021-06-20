from django.urls import path
from . import views
from TMC2 import settings
from django.conf import settings
from django.conf.urls.static import static

app_name = 'camp'

urlpatterns = [
    path('camp/', views.camps, name="camps"),
    path('camp/<int:pk>/',views.camp_page,name="camp"),
    path('camp/participant/<int:pk>/',views.reg_to_camp, name="reg_to_camp"),
]

