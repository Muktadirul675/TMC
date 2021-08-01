from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.


class Contest(models.Model):
    name = models.CharField(max_length=2000)
    type = models.CharField(max_length=50, choices=[
        ('Pre Registered', 'Pre Registered'),
        ('On Spot', 'On Spot'),
    ])
    time = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    date = models.CharField(max_length=1000)
    organizer = models.CharField(max_length=2000)
    code = models.CharField(max_length=30)
    description = RichTextField()
    total_questions = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


class Question(models.Model):
    question = models.CharField(max_length=2000)
    contest = models.ForeignKey(Contest, related_name='questions', on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)
    index = models.IntegerField()

    def __str__(self):
        return f'{self.question}'


class MCQQuestions(models.Model):
    question = models.CharField(max_length=2000)
    contest = models.ForeignKey(Contest, related_name='mcq_questions', on_delete=models.CASCADE)
    index = models.IntegerField()

    def __str__(self):
        return f'{self.question}'


class MCQOptions(models.Model):
    option = models.CharField(max_length=2000)
    question = models.ForeignKey(MCQQuestions, related_name='answers', on_delete=models.CASCADE)
    index = models.IntegerField()

    def __str__(self):
        return f'{self.answer} - {self.question}'

