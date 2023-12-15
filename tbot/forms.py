from django import forms
from .models import Tbot

class AddTbotForm(forms.ModelForm):
    class Meta:
        model = Tbot
        fields = ['name', 'description', 'link', 'token']
        labels = {
            'name': 'Bot Name',
            'description': 'Bot Description',
            'link': 'Bot Link',
            'token': 'Bot Token',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control m-2'}),
            'description': forms.TextInput(attrs={'class': 'form-control m-2'}),
            'link': forms.TextInput(attrs={'class': 'form-control m-2'}),
            'token': forms.TextInput(attrs={'class': 'form-control m-2'}),
        }
   