from django.urls import path
from . import views
from TMC2 import settings
from django.conf import settings
from django.conf.urls.static import static

app_name = 'contest'

urlpatterns = [
    path('contest/',views.conests, name="contests"),
]



