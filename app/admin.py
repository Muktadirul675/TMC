from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(
    (
        models.Problem,
        models.ProblemSolved,
        models.ProblemTried,
        models.Profile,
        models.Badge,
        models.ProblemTag,
        models.InRank,
    )
)
