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
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }


class MemberForm(forms.ModelForm):
    firstname = forms.CharField(label='First name', max_length=100)
    lastname = forms.CharField(label='Last name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)

    class Meta:
        model = Member
        fields = ['dob', 'address', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['firstname'].initial = self.instance.user.first_name
            self.fields['lastname'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        user = self.instance.user
        user.first_name = self.cleaned_data['firstname']
        user.last_name = self.cleaned_data['lastname']
        user.email = self.cleaned_data['email']
        user.save()
        return super().save(commit=commit)
