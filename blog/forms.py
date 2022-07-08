from django import forms
from .models import Comment, Post
# from django.contrib.auth.models import User
from django.conf import settings

class NowComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','title','body')
        
class PostCreateForm(forms.ModelForm):
    title = forms.CharField(label='عنوان التدوينة')
    # post_image = forms.ImageField(label='صورة المقال')
    content = forms.CharField(label='نص التدوينة', widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ['title','content']

