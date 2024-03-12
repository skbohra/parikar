from django.forms import ModelForm
from .models import * 

class NewParikForm(ModelForm):
    class Meta:
        model = Parik
        exclude = ["user","created_on"]

class NewChannelForm(ModelForm):
    class Meta:
        model = Channel
        exclude = ["owner","created_on","is_active","small_thumbnail"]
