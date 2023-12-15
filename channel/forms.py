from django import forms
from .models import Channel
from tbot.models import Tbot

class AddChannelForm(forms.ModelForm):
    tbot = forms.ModelChoiceField(queryset=Tbot.objects.all(), empty_label="[select bot...]" , required=True)
    class Meta:
        model = Channel
        fields = ['name', 'description', 'link' , 'tbot']
        labels = {
            'name': 'Channel Name',
            'description': 'Channel Description',
            'link': 'Channel Link',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control m-2'}),
            'description': forms.TextInput(attrs={'class': 'form-control m-2'}),
            'link': forms.TextInput(attrs={'class': 'form-control m-2'}),
            # 'tbot': forms.Select(attrs={'class': 'form-control m-2'}),
        }
   
class UpdateChannelForm(forms.ModelForm):
    tbot = forms.ModelChoiceField(queryset=Tbot.objects.all(), empty_label="[select bot...]", required=True)

    class Meta:
        model = Channel
        fields = ['name', 'description', 'link', 'tbot']
        labels = {
            'name': 'Channel Name',
            'description': 'Channel Description',
            'link': 'Channel Link',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control m-2'}),
            'description': forms.TextInput(attrs={'class': 'form-control m-2'}),
            'link': forms.TextInput(attrs={'class': 'form-control m-2'}),
        }



class AddPostForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        channel = kwargs.pop('channel', None)
        super(AddPostForm, self).__init__(*args, **kwargs)

        if channel:
            self.fields['channel'] = forms.ModelChoiceField(
                queryset=Channel.objects.filter(pk=channel.pk),
                widget=forms.HiddenInput(),
            )

