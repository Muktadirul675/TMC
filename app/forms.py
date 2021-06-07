from django import forms
from . import models

class Problem(forms.ModelForm):
    class Meta:
        model = models.Problem
        fields = "__all__"
        exclude = ('first_solve','problem_maker')
        labels = {
            'problem_name': 'Problem Name',
            'problem': 'Problem',
            'answer': 'Answer',
            'problem_hardness': 'Problem Hardness',
            'problem_cat': 'Problem Category',
            'point': 'Problem Point',
        }
        widgets = {
            'problem_name': forms.TextInput(attrs={'class':'form-control',}),
            'problem': forms.Textarea(attrs={'class':'form-control',}),
            'answer': forms.NumberInput(attrs={'class':'form-control',}),
            'point': forms.NumberInput(attrs={'class':'form-control'}) 
        }

class Camp(forms.ModelForm):
    class Meta:
        model = models.Camp()
        fields = "__all__"

        labels = {
            'name': 'Camp Name',
            'date': 'Camp Date',
            'camp_topic': 'Topic',
            'description': 'Description',
            'registration_fee': 'Registration Fee',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control',}),
            'date': forms.TextInput(attrs={'class':'form-control',}),
            'camp_topic': forms.TextInput(attrs={'class':'form-control',}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'registration_fee': forms.NumberInput(attrs={'class':'form-control'}),
        }



