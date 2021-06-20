from django.contrib import admin
from . import models

# Register your models here.

admin.site.register((
    models.Camp,
    models.CampTrainer,
    models.CampOrganizer,
    models.CampParticipant,
    models.CampAnnouncement,
    models.CampContest,
))
