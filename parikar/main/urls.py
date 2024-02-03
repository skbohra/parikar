from django.urls import path
from django.urls import re_path
from voting.views import vote_on_object

from . import views
from . import models 

widget_kwargs = {
    'model': models.Parik,
    'template_object_name': 'parik',
    'allow_xmlhttprequest': True,
}

urlpatterns = [
    path("", views.index, name="index"),
    path("play/<int:id>/", views.single_video, name="single_video"),
    path("new/", views.add_parik, name="add_parik"),
    path("search/", views.search, name="search"),
    re_path(
        r"^pariks/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$",
        vote_on_object,
        kwargs=widget_kwargs,
    ),
    ]
