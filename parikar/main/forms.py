from django.forms import ModelForm
from .models import * 

class NewParikForm(ModelForm):
    class Meta:
        model = Parik
        exclude = ["user","created_on"]
