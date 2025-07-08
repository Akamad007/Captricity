# flake8: noqa
from django.contrib.auth.models import User
from django.db import models
from home.models import HomeImages

# Create your models here.


class ApiBatch(models.Model):
    name = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.TextField(null=True, blank=True)
    submit = models.TextField(null=True, blank=True)
    progress = models.CharField(max_length=300, null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    success = models.BooleanField(default=False)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if self.status:
            return str(self.success) + " | " + str(self.id) + " | " + self.status
        else:
            return str(self.success) + " | " + str(self.id)


class ApiBatchImage(models.Model):
    batch = models.ForeignKey(ApiBatch, on_delete=models.CASCADE)
    image = models.ForeignKey(HomeImages, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now_add=True)


class ApiBatchData(models.Model):
    batch = models.ForeignKey(ApiBatch, on_delete=models.CASCADE)
    text = models.TextField()    dateTime = models.DateTimeField(auto_now_add=True)
