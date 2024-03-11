from django.contrib.contenttypes.models import ContentType
from django import template


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
