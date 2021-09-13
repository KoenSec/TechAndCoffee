from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image','posted_by']

class CommentForm(forms.ModelForm):
    class Meta:
        error_messages = {
                NON_FIELD_ERRORS:{
                    
                }
        }
        model = Comment
        fields = ['comment']