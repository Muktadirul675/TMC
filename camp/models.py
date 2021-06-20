from django.db import models
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.forms.models import model_to_dict
# Create your models here.

class Camp(models.Model):
    name = models.CharField(max_length=1000)
    date = models.CharField(max_length=1000)
    camp_topic = models.CharField(max_length=1000)
    description = RichTextField()
    banner = models.ImageField(upload_to="banners/")
    camp_logo = models.ImageField(upload_to="logos/")
    paid = models.CharField(max_length=20, choices=[
        ("Paid","Paid"),
        ("Free","Free"),
    ])
    registration_fee = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[
        ("Ongoing","Ongoing"),
        ("Upcoming","Upcoming"),
        ("Held","Held")
    ] , default="Upcoming")
    code = models.CharField(max_length=100)
    from_class = models.CharField(max_length=20,choices=
        [
            ("1","1"),
            ("2","2"),
            ("3","3"),
            ("4","4"),
            ("5","5"),
            ("6","6"),
            ("7","7"),
            ("8","8"),
            ("9","9"),
            ("10","10"),
            ("11","11"),
            ("12","12"),
        ]
    )
    to_class = models.CharField(max_length=20,choices=
        [
            ("1","1"),
            ("2","2"),
            ("3","3"),
            ("4","4"),
            ("5","5"),
            ("6","6"),
            ("7","7"),
            ("8","8"),
            ("9","9"),
            ("10","10"),
            ("11","11"),
            ("12","12"),
            ("12+","12+")
        ]
    )

    def __str__(self):
        return f"{self.name}"

class CampTrainer(models.Model):
    name = models.CharField(max_length=1000)
    camp = models.ForeignKey(Camp, related_name="trainers", on_delete=models.CASCADE)
    instituion = models.CharField(max_length=1000)
    work = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="camp_trainers/",default="/user.png")
    chief = models.BooleanField()

    def __str__(self):
        return f"{self.camp} {self.name} "

class CampOrganizer(models.Model):
    name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="camp_organizer/",default="/user.png")
    camp = models.ForeignKey(Camp,related_name="organizers",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class CampParticipant(models.Model):
    user = models.ForeignKey(User, related_name="campers", on_delete=models.CASCADE)
    camp = models.ForeignKey(Camp, related_name="campers", on_delete=models.CASCADE)
    reg_id = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    camper_class = models.CharField(max_length=20)
    camper_category = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} {self.reg_id} "

class CampAnnouncement(models.Model):
    user = models.ForeignKey(User, related_name="announces", on_delete=models.CASCADE)
    camp = models.ForeignKey(Camp, related_name="announces", on_delete=models.CASCADE)
    announce = RichTextField()
    time = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.camp} {self.user}"

class CampContest(models.Model):
    camp = models.ForeignKey(Camp, related_name="camp_contest", on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    status = models.CharField(max_length=20, choices=[
        ("Ongoing","Ongoing"),
        ("Upcoming","Upcoming"),
        ("Held","Held"),
    ])
    description = RichTextField()
    date = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.camp} {self.name}"

class CampContestParticipant(models.Model):
    user = models.ForeignKey(CampParticipant, related_name="c_campers", on_delete=models.CASCADE)
    point = models.IntegerField(default=0)
