from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    name = models.CharField(max_length=1000)
    article = RichTextField()
    added_by = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    banner = models.ImageField(upload_to='blog/articles/banners/')

    def __str__(self):
        return f'{self.name} - {self.added_by}'
