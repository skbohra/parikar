from django.contrib import admin

# Register your models here.
from .models import * 

admin.site.register(Parik)
admin.site.register(Font)
admin.site.register(FontColor)
admin.site.register(Animation)
admin.site.register(Channel)
admin.site.register(ChannelSubscriber)
