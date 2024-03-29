from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.filter
def content_type(obj):
    if not obj:
        return False
    return ContentType.objects.get_for_model(obj).name.replace(" ","_")
