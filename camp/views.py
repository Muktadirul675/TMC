from django.shortcuts import render, redirect
from . import models
import random

# Create your views here.

def camps(request):

    camps = models.Camp.objects.all()

    cont = {'camps':camps}

    return render(request,'event.html', cont)

def camp_page(request,pk):
    camp = models.Camp.objects.get(pk=pk)
    more_camp = [] 
    trainers = [] 
    chief = []
    announces = reversed(models.CampAnnouncement.objects.filter(camp=camp))
    already_reg = False
    classes = []
    contests = []
    ongoing = []
    upcoming = []
    held = []
    for i in camp.camp_contest.all():
        contests.append(i)
    for i in contests:
        if i.status == "Upcoming":
            upcoming.append(i)
        elif i.status == "Held":
            held.append(i)
        elif i.status == "Ongoing":
            ongoing.append(i)
    from_class = int(camp.from_class)
    to_class = None
    if camp.to_class == "12+":
        to_class = 12
    else:
        to_class = int(camp.to_class)

    for i in range(from_class, to_class+1):
        classes.append(str(i))
    if camp.to_class == "12+":
        classes.append("12+")

    for p in models.CampParticipant.objects.all():
        if p.user == request.user and p.camp == camp :
            already_reg = True
            break

    for i in models.CampTrainer.objects.filter(camp=camp):
        if i.chief == True:
            chief.append(i)
        else:
            trainers.append(i)

    for i in range(3):
        more_camp.append(random.choice(models.Camp.objects.all()))


    cont = {
        'camp': camp,
        'more_camps': more_camp,
        'trainers': trainers,
        'chiefs': chief,
        'announces':announces,
        'already_reg': already_reg,
        'classes':classes,
        'contests':reversed(contests),
        'ongoing':ongoing,
        'upcoming':upcoming,
        'held':held,
    }

    return render(request, './camp.html', cont)

def reg_to_camp(request,pk):
    if request.user.is_authenticated:
        camp = models.Camp.objects.get(pk=pk)
        participant = models.CampParticipant()
        participant.camp = camp
        participant.user = request.user

        def get_participant_id():
            count = 0
            for p in models.CampParticipant.objects.all():
                if p.camp == camp:
                    count += 1
                
            count += 1

            return count

        def make_reg_id(camp,category):
            code = camp.code
            category_code = None
            if category == "Primary":
                category_code = "P"
            elif category == "Junior":
                category_code = "J"
            elif category == "Senior":
                category_code = "S"
            elif category == "Intermediate":
                category_code = "I"

            return f"{code}{category_code}-{get_participant_id()}"

        participant.camper_class = request.POST['class']
        primary = [1,2,3,4,5]
        junior = [6,7,8]
        senior = [9,10,11,12]
        category = None
        if int(request.POST['class']) in primary:
            category = "Primary"
        if int(request.POST['class']) in junior:
            category = "Junior"
        if int(request.POST['class']) in senior:
            category = "Senior"
        
        if category == None:
            participant.camper_category = "Intermediate"
        else:
            participant.camper_category = category

        participant.reg_id = make_reg_id(camp, participant.camper_category)
        
        participant.save()

        return redirect(f"/camp/{pk}/")
    else:
        return redirect("tmc:user_login")
