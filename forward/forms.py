from django import forms
from post.models import Image
from .models import Forward
from channel.models import Channel
class ForwardForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True , 'class' : 'form-control m-2'}), required=False)
    channels = forms.ModelMultipleChoiceField(queryset=Channel.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control m-2'}))
    class Meta:
        model = Forward
        fields = ['name', 'description', 'content', 'scheduled_time', 'channels']
        labels = {
            'scheduled_time' : 'Scheduled Time (s)'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control m-2'}),
            'description': forms.TextInput(attrs={'class': 'form-control m-2'} ),
            'content': forms.Textarea(attrs={"rows":"5" , 'class' : 'form-control m-2'}),
        }