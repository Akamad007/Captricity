from celery import task
from Captricity.settings import PROJECT_PATH

@task()
def uploadAllImages():
    from captools.api import Client    
    from home.models import HomeImages
    from django.contrib.auth.models import User
    from Captricity.settings import CAPTRICITY_API_TOKEN, BATCH_NAME as STORED_BATCH_NAME, CAPTRICITY_TEMPLATE_NAME
    from api.views import get_random_batch_name,create_or_get_batch, status, submit
    from api.models import ApiBatch, ApiBatchImage
    
    users = User.objects.all()
    for user in users:
        images= HomeImages.objects.filter(user=user,is_active = True)            
        client = Client(CAPTRICITY_API_TOKEN)        
        BATCH_NAME = get_random_batch_name(STORED_BATCH_NAME)
    
        batch_id = create_or_get_batch(client,BATCH_NAME)        
        documents = client.read_documents()        
        document_id = filter(lambda x: x['name'] == CAPTRICITY_TEMPLATE_NAME, documents).pop()['id']
        client.update_batch(batch_id, { 'documents': document_id, 'name': BATCH_NAME })
        batchObject = ApiBatch.objects.create(name=BATCH_NAME,user = user)      
        batchObject.save()
        for image in images:
            f = open(PROJECT_PATH+"/../"+image.image.url, 'rb')
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
            print("Image saved")
        except Exception as e:
            batchObject.status = str(e)
            batchObject.submit = ""
            batchObject.success = False    
            print("Big werror")
        batchObject.save()


@task
def mailUser():
    from api.models import ApiBatch, ApiBatchData
    from captools.api import Client 
    from Captricity.settings import CAPTRICITY_API_TOKEN
    from django.core.mail import send_mail
    import ast
    batches = ApiBatch.objects.filter(success = True)
   
    for batch in batches:
        data  = ApiBatchData.objects.filter(batch = batch)
        if data.count() == 0:
            
            client = Client(CAPTRICITY_API_TOKEN)                          
            related_job_id = ast.literal_eval(batch.submit)['related_job_id'] 
           
            csv_out = client.read_job_results_csv(related_job_id)               
            data = ApiBatchData.objects.create(batch=batch,text = csv_out)               
            data.save()
            send_mail('Captricity data completed.', 'Your data is completed. The link for the data is http://localhost:8000/api/data/'+str(batch.id)+"/", 'akashdeshpande2000@gmail.com',
                      [batch.user.email], fail_silently=False) 
            
            
        else:
            pass
        