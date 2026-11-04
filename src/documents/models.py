from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

User = settings.AUTH_USER_MODEL



class Document(models.Model):
    owner =  models.ForeignKey(User,on_delete=models.CASCADE)
    title =  models.CharField(default="Title",max_length=500)
    content = models.TextField(blank=True,null=True)
    active = models.BooleanField(default=True)
    activated_at= models.DateTimeField(auto_now_add=False,auto_now=False,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)  

def save(self, *args, **kwargs):
    if self.active:
        if self.activated_at is None:
            self.activated_at = timezone.now()
    else:
        self.activated_at = None

    super().save(*args, **kwargs)