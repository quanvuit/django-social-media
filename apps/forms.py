from django import forms
from .models import Post, Comment, Member

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['dob', 'address', 'avatar']
