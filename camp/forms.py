from django import forms

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