from django.shortcuts import render,redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import random
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
# Create your views here.
def containsLetterAndNumber(input):
    return input.isalnum() and not input.isalpha() and not input.isdigit()

def register(request):
    if request.method=="POST":
        
        user1=request.POST.get('user')
        pass1=request.POST.get('pass')
        pass2=request.POST.get('pass1')
        #print(type(pass1))
        #pass2=str(pass2)

        if pass1==pass2:
            if User.objects.filter(username=user1).exists():
                error_messages={"message1":"User already exists!"}
                return render(request,"app/register.html",context=error_messages)
            
            elif (containsLetterAndNumber(pass1)==False):
                error_messages={"message1":"Password should be in alphanum only!"}
                return render(request,"app/register.html",context=error_messages)
            
            elif(len(pass1)<8):
                error_messages={"message1":"Password too short! Should be at least 8 characters long!!"}
                return render(request,"app/register.html",context=error_messages)

            else:
                user=User.objects.create_user(username=user1,password=pass1)
                user.save()
                #login(request,user)
                return render(request,"app/yes.html",{"user1":user1})
        else:
            error_messages={"message1":"Passwords do not match"}
            return render(request,"app/register.html",context=error_messages)

        
    return render(request,"app/register.html")

def lin(request):
    if request.method=="POST":
        user1=request.POST.get('user')
        pass1=request.POST.get('pass')
        user=authenticate(username=user1, password=pass1)
        if user is not None:
            if user.is_active:
                login(request,user)
                response=redirect("/index/")
                return response
                
        else:
            error_messages={"message1":"Invalid Credentials"}
            return render(request,"app/login.html",context=error_messages)

    return render(request,"app/login.html")

@login_required(login_url="/lin/")
def index(request):
    user = request.user
    profile=Profile.objects.filter(user=user)
    return render(request,"app/index.html",{"profile":profile})

@login_required(login_url="/lin/")
def create(request):
    user=request.user
    profile=Profile(user=user)
    if request.method=="POST" and request.FILES['image']:
        detail1=request.POST.get('detail')
        img=request.FILES['image']
        permit1=request.POST.get('permit')
        if(permit1=="private"):
            profile.permit=False
        else:
            profile.permit=True
        profile.detail=detail1
        profile.image=img
        profile.save()
        return render(request,"app/create.html",{"message1":"Blog created successfully"})
    return render(request,"app/create.html")

@login_required(login_url="/lin/")
def search(request):
    myuser=request.user
    if request.method=="POST":
        user1=request.POST.get('username')
        if User.objects.filter(username=user1).exists():
            if(user1==myuser.username):
                return redirect("/index/")
            else:
                user2=User.objects.filter(username=user1).first()
                profile=Profile.objects.filter(user=user2,permit=True)
                return render(request,"app/search_result.html",{"profile":profile})
        else:
            return render(request,"app/search.html",{"message1":"User does not exist!"})
    return render(request,"app/search.html")


def log(request):
    logout(request)
    return redirect("/lin/")