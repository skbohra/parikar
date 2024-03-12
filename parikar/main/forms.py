from django.forms import ModelForm
from .models import * 
from django.forms.widgets import TextInput

class NewParikForm(ModelForm):
    class Meta:
        model = Parik
        exclude = ["user","created_on"]
        widgets = {
                   'color': TextInput(attrs={'type': 'color'}),
                   'background': TextInput(attrs={'type': 'color'}),
                   }

class NewChannelForm(ModelForm):
    class Meta:
        model = Channel
        exclude = ["owner","created_on","is_active","small_thumbnail"]
