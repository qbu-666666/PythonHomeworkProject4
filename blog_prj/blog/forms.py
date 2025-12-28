from django import forms
from .models import BlogPost, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'cover_image', 'tags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': '写下你的评论...'})
        }
        labels = {
            'text': ''
        }