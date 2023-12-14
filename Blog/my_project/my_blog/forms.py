from django import forms
from django.forms import Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment

class UserRegisterForm(UserCreationForm):
    email= forms.EmailField()

    class Meta:
        model =User
        fields = ['username','email','password1','password2']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude=["post"]
        labels = {
            "user_name" : "Your Name",
            "user_email" : "Your Email",
            "text" : "Your Comment"
        }
        widgets = {    #if we don't use widgets our text area for comments is going out of body
            "text": Textarea(attrs={'rows': 3})
        }