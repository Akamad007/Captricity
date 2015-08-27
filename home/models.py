from django.db import models
from django.contrib.auth.models import User
import hashlib

import random, string

# Create your models here.
def get_photo_storage_path(photo_obj, filename):    
     
    random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    storage_path = 'img/home/' + random_string +"_"+hashlib.sha1(str(photo_obj.user.id)).hexdigest()  +'_' + filename
    return storage_path 


class HomeImages(models.Model):
    image = models.ImageField(upload_to = get_photo_storage_path)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200, blank = True, null= True)
    title = models.CharField(max_length = 200, blank = True, null= True)
    is_active = models.BooleanField(default = True)
    datetime = models.DateTimeField(auto_now_add=True)
    
        
    
    
    