from django.shortcuts import render,redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
import random
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
# Create your views here.

def containsLetterAndNumber(input):
    return input.isalnum() and not input.isalpha() and not input.isdigit()

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('/lin/')
    else:
        form = SignUpForm()

    return render(request,"app/register.html",{"form":form})

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
        user1=request.POST.get('ans')
        if User.objects.filter(username=user1).exists():
            if(user1==myuser.username):
                return redirect("/index/")
            else:
                user2=User.objects.filter(username=user1).first()
                profile=Profile.objects.filter(user=user2,permit=True)
                return render(request,"app/search_result.html",{"profile":profile,"user":user2})
        else:
            return render(request,"app/base.html",{"message1":"User does not exist!"})
    return render(request,"app/search.html")


def log(request):
    logout(request)
    return redirect("/lin/")