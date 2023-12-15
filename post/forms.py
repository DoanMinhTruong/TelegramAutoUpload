from django import forms
from .models import Post, Image

class PostForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True , 'class' : 'form-control m-2'}), required=False)
    class Meta:
        model = Post
        fields = ['name', 'description', 'content', 'scheduled_time']
        labels = {
            'scheduled_time' : 'Scheduled Time (s)'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control m-2'}),
            'description': forms.TextInput(attrs={'class': 'form-control m-2'}),
            'content': forms.Textarea(attrs={"rows":"5" , 'class' : 'form-control m-2'}),
        }
# PostImageFormSet = inlineformset_factory(Post, PostImage, form=ImageForm, extra=1, can_delete=False)
