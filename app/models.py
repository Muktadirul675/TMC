from django.contrib.auth import default_app_config

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.forms.models import model_to_dict

# Create your models here.

class Problem(models.Model):
    problem_name = models.CharField(max_length=500)
    problem = RichTextField()
    time = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    answer = models.FloatField()
    problem_hardness = models.CharField(max_length=20,choices=[
        ('Hard','Hard'),
        ('Easy','Easy'),
        ('Medium','Medium'),
        ('Intermediate','Intermediate')
    ])
    problem_maker = models.CharField(max_length=1000)
    first_solve = models.CharField(max_length=1000,null=True,default="None")
    problem_cat = models.CharField(max_length=20, choices=[
        ("Math","Math"),
        ("Physics","Physics")
    ])
    point = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.problem_name}"

class ProblemTag(models.Model):
    name = models.CharField(max_length=100)
    problem = models.ForeignKey(Problem, related_name="tags",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.problem}"

class ProblemSolved(models.Model):
    problem = models.ForeignKey(Problem, related_name="solved",on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.problem.id} {self.user.username}"

class ProblemTried(models.Model):
    problem = models.ForeignKey(Problem, related_name="tried",on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    ans = models.FloatField()
    def __str__(self):
        return f"{self.problem.id} {self.user.username}"

class Profile(models.Model):
    user = models.ForeignKey(User,related_name="profile",on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image/",default="/user.png",null=True,blank=True)
    bio = models.CharField(max_length=2000,null=True, blank=True)
    address = models.CharField(max_length=1000,null=True, blank=True)
    institution = models.CharField(max_length=1000,null=True, blank=True)
    work = models.CharField(max_length=1000,null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    contact_no = models.CharField(max_length=20,null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    update = models.DateTimeField(auto_now=True,null=True, blank=True)
    point = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Badge(models.Model):
    user = models.ForeignKey(User,related_name="badge",on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    level = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class InRank(models.Model):
    user = models.ForeignKey(User, related_name='inrank',on_delete=models.CASCADE)


