import re
from django.contrib.messages.api import error
from django.shortcuts import render, HttpResponse,redirect, get_object_or_404
from .models import *
from django.contrib import messages
import bcrypt
from .forms import *




def loginPage(request):
    return render(request,"loginPage.html")

def homePage(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'this_user':User.objects.get(id = request.session['user_id']),

        }
    return render(request,"homePage.html",context)

def register(request):
    
    if request.method != "POST":
        return redirect('/')
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt(15)).decode()

    # creating a new user
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name =request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_pw
    )
    #store users id in request.session
    request.session['user_id'] = new_user.id
    return redirect('/homePage')

def login(request):
    
    if request.method != "POST":
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    this_user = User.objects.filter(email = request.POST['email'])[0]
    request.session['user_id'] = this_user.id
    messages.success(request, "Your Logged In Congrats !")
    return redirect('/homePage')

def logout(request):
    request.session.flush()
    return redirect('/')

def new(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'this_user':User.objects.get(id = request.session['user_id'])
    }
    return render(request,"newPost.html",context)

def imageview(request):
    if request.method =='POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = PostForm()
    return render(request,'image_upload.html', {'form' : form})

def displayImages(request):
    if request.method == 'GET':
        Posts = Post.objects.all()
        return render(request, 'viewPosts.html',{'Post_images' : Posts})

def success(request):
    return HttpResponse('successfully uploaded')

def createComment(request):
    post = get_object_or_404(Post,pk = request.POST["Post_id"])
    # print(post)
    # comments = Comment.objects.get(post=post)
    if request.method == 'POST':
        Comment_Form = CommentForm(data = request.POST)
        if Comment_Form.is_valid():
            new_comment = Comment_Form.save(commit=False)
            new_comment.user = User.objects.get(id = request.session["user_id"])
            new_comment.post = post
            new_comment.save()
    else:
        Comment_Form = CommentForm()
    return redirect("/homePage/viewPosts")

def editComment(request,comment_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context ={
        "comment_to_edit":Comment.objects.get(id = comment_id),
        'this_user':User.objects.get(id = request.session['user_id'])
    }
    return render(request,"editPage.html",context)

def updateComment(request,comment_id):
    if 'user_id' not in request.session:
        return redirect('/')
    commenttochange = Comment.objects.get(id = comment_id)
    form = CommentForm(request.POST,instance = commenttochange)
    print()
    if form.is_valid():
        form.save()
    return redirect("/homePage/viewPosts")

def profileView(request,user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'this_user':User.objects.get(id = request.session['user_id']),
        'this_users_comments':User.objects.get(id = user_id).usercomment.all()
    }
    return render(request,"profilePage.html",context)




    