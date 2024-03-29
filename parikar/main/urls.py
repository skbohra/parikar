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
    path("play/instant/", views.instant_video, name="instant_video"),
    path("channel/<int:id>/", views.channel_view, name="channel"),
    path("new/", views.add_parik, name="add_parik"),
    path("accounts/profile/", views.new_channel, name="new_channel"),
    path("instant/save/<int:id>/", views.save_instant, name="save_instant"),
    path("search/", views.search, name="search"),
    path("explore/", views.explore, name="explore"),
    path("subscription/", views.subscription, name="subscription"),
    path("subscribe/<int:id>/", views.subscribe_channel, name="subscribe_channel"),
    re_path(
        r"^pariks/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$",
        vote_on_object,
        kwargs=widget_kwargs,
    ),
    path("record/view_stat/<int:id>/", views.record_post_view, name="record_post_view"),
    path("edit/post/<int:id>/", views.edit_parik, name="edit_post"),
    path("channels/", views.channels, name="channels"),
    ]
