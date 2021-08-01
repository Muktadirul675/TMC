from django.shortcuts import render

# Create your views here.

def conests(request):

    cont = {}

    return render(request, 'under_construction.html', cont)
