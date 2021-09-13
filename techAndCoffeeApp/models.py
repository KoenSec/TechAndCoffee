from django.db import models
from django.http import request
import re
import bcrypt

class Usermanager(models.Manager):
    def register_validator(self,post_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(post_data['first_name'])==0:
            errors['first_name'] = "First Name is Required"
        if len(post_data['last_name'])==0:
            errors['last_name'] = "Last Name is Required"
        if len(post_data['email'])==0:
            errors['email'] = "Email is Required"
        if len(post_data['password']) < 8:
            errors['password'] = "Password is Required"
        if post_data['password']!= post_data['confirm_password']:
            errors['match']= "Passwords do not match"
        return errors
    
    def login_validator(self,post_data):
        errors = {}
        existing_user = User.objects.filter(email = post_data['email'])
        if len(post_data['email'])==0:
            errors['email'] = "Email is Required"
        elif len(existing_user) ==0:
            errors['does_not_exist'] = "Please enter a valid Email and Password"
        if len(post_data['password']) < 8:
            errors['password'] = "Password Must be at least 8 characters long !"   
        elif not bcrypt.checkpw(post_data['password'].encode(), existing_user[0].password.encode()):
            errors['mismatch'] = "Please enter a valid Email and Password"
        return errors

class Commentmanager(models.Manager):
    def comment_validator(self,post_data):
        errors={}
        if len(post_data['comment']) < 1:
            errors['comment'] = "wall comment must be longer than 1 character!!!"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Usermanager()


class Post(models.Model):
    posted_by = models.ForeignKey(User, related_name="posts_uploaded", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Comment(models.Model):
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, related_name="postcomment", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name="usercomment", on_delete = models.CASCADE)
    objects = Commentmanager()




