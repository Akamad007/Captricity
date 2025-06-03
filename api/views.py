# Create your views here.
from captools.api import Client
from django.contrib import messages

import captools.api
from Captricity.settings import CAPTRICITY_API_TOKEN_SUBMIT,CAPTRICITY_API_TOKEN, BATCH_NAME as STORED_BATCH_NAME, CAPTRICITY_TEMPLATE_NAME

import random, string
from api.models import ApiBatch, ApiBatchImage, ApiBatchData
from home.models import HomeImages
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def add(request, id):
    try:
        image = HomeImages.objects.get(id = int(id),user=request.user,is_active = True)
    except:
        messages.error(request, "Error. Did not find the image object")
        return HttpResponseRedirect("/home/")
    client = Client(CAPTRICITY_API_TOKEN_SUBMIT)        
    BATCH_NAME = get_random_batch_name(STORED_BATCH_NAME)
    batch_id = create_or_get_batch(client,BATCH_NAME)        
    documents = client.read_documents()
    
    document_id = filter(lambda x: x['name'] == CAPTRICITY_TEMPLATE_NAME, documents).pop()['id']
    client.update_batch(batch_id, { 'documents': document_id, 'name': BATCH_NAME })
    f = open(image.image.url, 'rb')
    batch_file = client.create_batch_files(batch_id, {'uploaded_file': f})
    batchObject = ApiBatch.objects.create(name=BATCH_NAME,user = request.user)
    try:
        batchObject.status = status(client,batch_id)
        batchObject.submit = submit(client,batch_id)
        batchObject.success = True
        messages.success(request, "The image was successfully added to batch "+batchObject.name)
    except Exception as e:
        batchObject.status = str(e)
        batchObject.submit = ""
        batchObject.success = False
        messages.success(request, "There was an Error in the batch "+batchObject.name+" "+str(e))
    
    batchObject.save()
    imageObject = ApiBatchImage.objects.create(batch = batchObject, image = image)
    imageObject.save()
    return HttpResponseRedirect("/home/")
    
    
def get_random_batch_name(STORED_BATCH_NAME):
    BATCH_NAME = STORED_BATCH_NAME+"".join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))  
    return BATCH_NAME
    
def create_or_get_batch(client, BATCH_NAME):
    try:
        batch = client.create_batches({'name': BATCH_NAME})
    except:
        pass
    
    batches = client.read_batches()
    batch_id = filter(lambda x: x['name'] == BATCH_NAME, batches).pop()['id']
    batch = client.read_batch(batch_id)
    return batch_id

def submit(client,batch_id):
    
    submitted_batch = client.submit_batch(batch_id, {})
    
    return submitted_batch

def status(client,batch_id):
    batch_ready_status = client.read_batch_readiness(batch_id)
    if len(batch_ready_status['errors']) > 0:               
        raise Exception(batch_ready_status['errors'][0])
    else:      
        return batch_ready_status['status']
        
@login_required
def addall(request):
    try:
        images= HomeImages.objects.filter(user=request.user,is_active = True)
    except:
        messages.error(request, "Error. Did not find the image object")
        return HttpResponseRedirect("/home/")
    client = Client(CAPTRICITY_API_TOKEN_SUBMIT)        
    BATCH_NAME = get_random_batch_name(STORED_BATCH_NAME)

    batch_id = create_or_get_batch(client,BATCH_NAME)        
    documents = client.read_documents()
    
    document_id = filter(lambda x: x['name'] == CAPTRICITY_TEMPLATE_NAME, documents).pop()['id']
    client.update_batch(batch_id, { 'documents': document_id, 'name': BATCH_NAME })
    batchObject = ApiBatch.objects.create(name=BATCH_NAME,user = request.user)
  
    batchObject.save()
    for image in images:
        f = open(image.image.url, 'rb')
        try:
            batch_file = client.create_batch_files(batch_id, {'uploaded_file': f})
            imageObject = ApiBatchImage.objects.create(batch = batchObject, image = image)
            imageObject.save()
        except:
            pass            
    try:
        batchObject.status = status(client,batch_id)
        batchObject.submit = submit(client,batch_id)
        batchObject.success = True
        messages.success(request, "All images were successfully added to batch "+batchObject.name+" total images "+str(images.count()))
    except Exception as e:
        batchObject.status = str(e)
        batchObject.submit = ""
        batchObject.success = False
        messages.success(request, "There was an Error in the batch "+batchObject.name+" "+str(e))
    batchObject.save()
    return HttpResponseRedirect("/home/")


@login_required
def view_all_batches(request):
    success_batches = ApiBatch.objects.filter(user = request.user, success = True).order_by("-dateTime")
    failure_batches = ApiBatch.objects.filter(user = request.user, success = False).order_by("-dateTime")
    return render(request,"api/batches.html",{"success_batches":success_batches,'failure_batches':failure_batches})

@login_required
def view_batch(request,id):
    try:
        batch = ApiBatch.objects.get(user = request.user,id=int(id))
        images = ApiBatchImage.objects.filter(batch = batch)
    except:
        pass
    
    return render(request,"api/batch.html",{"batch":batch,"images":images})

import ast
@login_required
def data(request,id):
    batch = None
    data = None
    try:
        batch = ApiBatch.objects.get(user = request.user,id=int(id))
        if batch.success:
            try:
                data = ApiBatchData.objects.get(batch = batch) 
            except:
                pass      
            if not data:                
                client = Client(CAPTRICITY_API_TOKEN)
                BATCH_NAME = batch.name                
                related_job_id = ast.literal_eval(batch.submit)['related_job_id']                              
                csv_out = client.read_job_results_csv(related_job_id)                              
                data = ApiBatchData.objects.create(batch=batch,text = csv_out)               
                data.save()              
        else:
            raise Exception("Batch was not successfull")          
    except:
        
        batch.status = "Error while extracting data"
        batch.save()
        messages.error(request, "There was an error in the batch")
        return HttpResponseRedirect("/home/")
    data = data.text.splitlines()
    for n,d in enumerate(data):
        data[n] = d.split(",")    
    messages.success(request, "The data was extracted successfully")        
    return render(request,"api/data.html",{"data":data,"batch":batch})