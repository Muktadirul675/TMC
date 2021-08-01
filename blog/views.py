from django.shortcuts import render
from . import models

# Create your views here.

def home(request):

    blogs = models.Article.objects.all()

    cont = {'blogs':blogs}

    return render(request, 'under_construction.html', cont)
