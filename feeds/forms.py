from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={
            'rows': 3, 'placeholder': 'Write what interests you here...'
        }))
    class Meta:
        model = Post
        fields = ['body', 'image']


class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 1, 'placeholder':  'Add comment here...'}))
    class Meta:
        model = Comment
        fields = ['body',]
