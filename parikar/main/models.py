from django.db import models

from django.contrib.auth.models import * 
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from PIL import Image 
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from mimetypes import guess_type
import os

from django.core.files.base import ContentFile

class Font(models.Model):
    font_name = models.CharField(max_length=50)


class FontColor(models.Model):
    hexcode = models.CharField(max_length=7) 

class Animation(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class PostViewStat(models.Model):
    view_progress = models.FloatField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    last_viewed_time = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

class Parik(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200,null=True,blank=True)
    content = models.TextField()
    created_on = models.DateTimeField()
    tags = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnails",null=True,blank=True)
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
    post_view_stat = GenericRelation(PostViewStat)
    summary = models.TextField(null=True,blank=True)
    def get_absolute_url(self):
        return f"/play/{self.id}/"



class Channel(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=100)
    about = models.TextField(null=True,blank=True)
    url = models.URLField(null=True,blank=True,verbose_name='Website')
    thumbnail = models.ImageField(upload_to="thumbnails")
    small_thumbnail = models.ImageField(upload_to="small_thumbnails",null=True,blank=True)
    created_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    @property
    def subscribers(self):
        subscribers = ChannelSubscriber.objects.filter(channel=self,is_active=True).count()
        return subscribers
    def create_channel_thumbnail(self):
        image = Image.open(self.thumbnail)
        image.thumbnail((64,64), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.thumbnail.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.small_thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


    def save(self, *args, **kwargs):
        self.create_channel_thumbnail()
        return super().save(*args, **kwargs)

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
    post_view_stat = GenericRelation(PostViewStat)
    def get_absolute_url(self):
        return f"/play/instant/?url={self.url}/"

    
class ServiceAPI(models.Model):
    service_name = models.CharField(max_length=100)
    url = models.URLField()
    api_key = models.CharField(max_length=200)


class Hope(models.Model):
    service_name = models.CharField(max_length=100)
    url = models.URLField()
    api_key = models.CharField(max_length=200)



