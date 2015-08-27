# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.forms import HomeImageForm
from home.models import HomeImages
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.utils.html import strip_tags

@login_required
def home(request):    
    images = HomeImages.objects.filter(is_active = True, user = request.user)
    return render(request,"home/home.html",{'images':images})

@login_required
def delete(request,id):    
    try:
        image = HomeImages.objects.get(user = request.user,is_active = True,id = int(id))
        image.is_active = False
        image.save()
        messages.success(request, "Image deleted successfully")        
    except:
        messages.error(request, "Image Not found")
    return HttpResponseRedirect("/home/")



@login_required
def create(request, id = None):
    images = HomeImages.objects.filter(is_active = True, user = request.user)
    try:
        image = HomeImages.objects.get(id = int(id), user = request.user)
    except:
        if id is not None:
            return HttpResponseRedirect("/home/create/")
        else:
            image = None
    if request.method == "POST":
        if image:
            imageForm = HomeImageForm(request.POST, request.FILES, instance = image)
        else:
            imageForm = HomeImageForm(request.POST, request.FILES)
        if imageForm.is_valid():
            imageObject = imageForm.save(commit = False)
            imageObject.user = request.user
            imageObject.title = strip_tags(imageObject.title)
            imageObject.save()                
    else:
        if image:
            imageForm = HomeImageForm(instance = image)
        else:
            imageForm = HomeImageForm()   
    return render(request,"home/create.html",{"imageForm":imageForm,'images':images,"image":image})
 