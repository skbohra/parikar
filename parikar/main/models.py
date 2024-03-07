from django.db import models

from django.contrib.auth.models import * 
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation


class Font(models.Model):
    font_name = models.CharField(max_length=50)


class FontColor(models.Model):
    hexcode = models.CharField(max_length=7) 

class Animation(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Parik(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200,null=True,blank=True)
    content = models.TextField()
    created_on = models.DateTimeField()
    tags = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnails")
    to_wrap = models.BooleanField(default=False)
    font = models.CharField(max_length=100,default="inherit")
    font_size = models.FloatField(default=0.6)
    color = models.CharField(max_length=100,default="#ffffff")
    background = models.CharField(max_length=100,default="#222222")
    font_weight = models.IntegerField(default=100)
    animation = models.ForeignKey(Animation,on_delete=models.CASCADE,blank=True,null=True)
    shuffle_colors_by_line  = models.BooleanField(default=False)
    shuffle_fonts_by_line  = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')

    def get_absolute_url(self):
        return f"/play/{self.id}/"



class Channel(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=100)
    about = models.TextField()
    url = models.URLField()
    thumbnail = models.ImageField(upload_to="thumbnails")
    created_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    @property
    def subscribers(self):
        subscribers = ChannelSubscriber.objects.filter(id=self.id,is_active=True).count()
        return subscribers


class ChannelSubscriber(models.Model):
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User,on_delete=models.CASCADE)
    subscribed_on = models.DateTimeField(auto_now = True)
    is_active = models.BooleanField(default=True)


class InstantParik(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200,null=True,blank=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    tags = models.TextField()
    is_user_saved = models.BooleanField(default=False)
    parik = models.ForeignKey(Parik,null=True,blank=True,on_delete=models.CASCADE)
    def get_absolute_url(self):
        return f"/play/instant/?url={self.url}/"

    
class ServiceAPIKEY(models.Model):
    service_name = models.CharField(max_length=100)
    url = models.URLField()
    api_key = models.CharField(max_length=200)
