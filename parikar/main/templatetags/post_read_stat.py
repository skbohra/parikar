from django.contrib.contenttypes.models import ContentType
from django import template

from main.models import ChannelSubscriber
register = template.Library()

@register.filter
def get_progress(obj,user):
    if not obj:
        return False
    try:
        view_progress = obj.post_view_stat.get(user=user).view_progress
    except:
        view_progress = 0.0
    return view_progress



@register.filter
def is_subscribed(obj,user):
    if not obj:
        return False
    try:
        ChannelSubscriber.objects.get(channel=obj,subscriber=user,is_active=True)
        is_subscribed = True
    except ChannelSubscriber.DoesNotExist:
        if obj.owner == user:
            is_subscribed = True
        else:
            is_subscribed = False
    return is_subscribed
