
# Create your views here.
from login.forms import LoginForm, SignUpForm
from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from django.contrib.auth.models import User


def logout(request):
    messages.success(request, "You have been logged out.")
    django_logout(request)
    
    return HttpResponseRedirect("/login/")

def login(request):
    
    if request.user.is_anonymous:
        if request.method == "POST":
            loginForm = LoginForm(request.POST)
            if loginForm.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:                   
                        django_login(request, user)
                        messages.success(request, "Successfull logged in")
                        return HttpResponseRedirect("/home/")    
        else:
            loginForm = LoginForm()
        return render(request,"login/login.html",{"loginForm":loginForm})
    else:
        return HttpResponseRedirect("/home/")


def signup(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            signupForm = SignUpForm(request.POST)
            if signupForm.is_valid():
                signupForm = signupForm.clean()
                
                userName = signupForm['username']
                userMail = signupForm['email']
                password = signupForm['password']
                user = User.objects.create_user(userName, userMail, password)
                user.save() 
                                       
                django_login(request, user)
                messages.success(request, "User account created succesfully")
                return HttpResponseRedirect('/home/')
            else:
                messages.error(request, "Please check the entered form")
        else:
            signupForm = SignUpForm()
        return render(request,"login/signup.html",{"signupForm":signupForm})
    else:
        return HttpResponseRedirect("/home/")