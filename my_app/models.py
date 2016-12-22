from django.db import models
from django.contrib.auth.models import User
# Create your models here.

default_image_path = 'images/default.jpg'

class Show(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    groups = models.CharField(max_length=45,default='')
    place = models.CharField(max_length=45,default='')
    datetime = models.DateTimeField(default='')
    image_url = models.CharField(default=default_image_path,max_length=256,null=False)
    participation = models.ManyToManyField(User)

    class Meta():
        db_table = 'shows'