from django.db import models

from django.contrib.auth.models import * 

class Parik(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_on = models.DateTimeField()
    tags = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnails")
    to_wrap = models.BooleanField(default=False)
    font = models.CharField(max_length=100,default="inherit")
    font_size = models.IntegerField(default=30)
    color = models.CharField(max_length=100,default="#ffffff")
    background = models.CharField(max_length=100,default="#222222")
    font_weight = models.IntegerField(default=100)
    animation_type = models.CharField(max_length=100,default="default")

    def get_absolute_url(self):
        return f"/play/{self.id}/"

