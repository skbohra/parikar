from django.shortcuts import *
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse
import textwrap
from .models import * 
from .forms import * 
import datetime 
from django.contrib.auth.decorators import login_required
from hitcount.views import * 
from .utils import *
from .tasks import * 
from django.core.paginator import Paginator
from el_pagination.decorators import page_template
import re
import base64
from django.core.files.base import ContentFile
import random
import string
from django.contrib import messages

DEFAULT_LINE_COLOR = ""
DEFAULT_LINE_FONT = ""

@login_required
@page_template('homepage_videos_list.html')  # just add this decorator
def index(request,extra_context=None,template="index.html"):
    subscribed_channels = []
    if request.user.is_authenticated:
        subscribed_channels = ChannelSubscriber.objects.filter(subscriber=request.user)

    pariks = Parik.objects.all().order_by('-id')
    paginator = Paginator(pariks, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {'pariks':page_obj,'subscribed_channels':subscribed_channels}
    return render(request, template, context)

@page_template('videos_list.html')  # just add this decorator
def single_video(request,id=id,extra_context=None,template="play-video.html"):
    parik = get_object_or_404(Parik,id=id)
    #keywords = extract_keywords_bert(parik.content)
    #print(keywords)
    tags = parik.tags.split(" ")
    if not parik.thumbnail:
        api_key = ServiceAPI.objects.get(service_name="stability")
        data = stability_text_to_image(parik.title,api_key)
        
        for i, image in enumerate(data["artifacts"]):
            data = ContentFile(base64.b64decode(image["base64"])) 
            uuid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            file_name = api_key.service_name+"_generated_"+ uuid + ".png"
            parik.thumbnail.save(file_name, data, save=True)
    if parik.to_wrap:
        lines = []
        #new_lines = parik.content.split(".")
        new_lines = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', parik.content)

        for line in new_lines:
            new_line = textwrap.wrap(line,width=50)
            lines = lines + new_line

    else:
        lines = parik.content.strip().split("\n")

    alldata = []



    i = 1 
    for line in lines:
        data = {}
        data['line'] = line
        if parik.shuffle_fonts_by_line:
            data['font'] = get_random_font()
        else:
            data['font'] = parik.font
        if parik.shuffle_colors_by_line:
            data['color'] = get_random_color()
        else:
            data['color'] = parik.color
        data['line_id'] = "line-%d_%d" % (parik.id,i)  
        alldata.append(data)
        i = i + 1 
    try:
        ChannelSubscriber.objects.get(channel=parik.user.channel,subscriber=request.user,is_active=True)
        is_subscribed = True
    except: #ChannelSubscriber.DoesNotExist:
        if parik.user == request.user:
            is_subscribed = True
        else:
            is_subscribed = False
    hit_count = HitCount.objects.get_for_object(parik)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    pariks = Parik.objects.all().exclude(id=id).order_by('-id')
    paginator = Paginator(pariks, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {'parik':parik,'tags':tags,'lines':alldata,'pariks':page_obj,'is_subscribed':is_subscribed,'now':datetime.datetime.now()}
    return render(request, template, context)

@login_required
def add_parik(request):
    form = NewParikForm()
    if request.method == "POST":
        form = NewParikForm(request.POST,request.FILES)
        if form.is_valid():
            parik = form.save(commit=False)
            parik.user = request.user
            parik.created_on = datetime.datetime.now()
            parik.save()
            return HttpResponseRedirect(reverse("single_video", args=[parik.id])) 
    pariks = Parik.objects.all().order_by('-id')
    context = {'form':form,'pariks':pariks}
    return render(request, "new-parik.html", context)


@login_required
def search(request):
    term = request.GET['query']
    pariks = Parik.objects.filter(title__icontains=term,tags__icontains=term)
    context = {'pariks':pariks,'query':term}
    return render(request, "search.html", context)



@login_required
def subscribe_channel(request,id):
    channel = get_object_or_404(Channel,id=id)
    if channel.owner == request.user:
        message = {'message': 'Sorry you cannot subscribe your own channel','type':'error'}
    else:
        try:
            channel_subscriber = ChannelSubscriber.objects.get(channel=channel,subscriber=request.user)
            if channel_subscriber.is_active:
                channel_subscriber.is_active = False
                channel_subscriber.save()
                message = {'message': 'Channel Unsubscribed','type':'success','btn_text':'Subscribe'}
            else:
                channel_subscriber.is_active = True
                channel_subscriber.save()
                message = {'message': 'Channel Subscribed','type':'success','btn_text':'Subscribed'}
        except ChannelSubscriber.DoesNotExist:
            channel_subscriber = ChannelSubscriber(channel=channel,subscriber=request.user,is_active=True)
            channel_subscriber.save()
            message = {'message': 'Channel Subscribed','type':'success','btn_text':'Subscribed'}
            print(e)
        print(message)
    return JsonResponse(message)

@login_required
def channel_view(request,id):
    channel = get_object_or_404(Channel,id=id)
    context = {'channel': channel}
    return render(request, "channel.html", context)


from bs4 import BeautifulSoup
import requests
import trafilatura


@page_template('videos_list.html')  # just add this decorator
def instant_video(request,extra_context=None,template="play-video.html"):
    url = request.GET.get("url", None)
    if not url:
        return render(request,'instant-url.html')
    else:

        try:
            instant = InstantParik.objects.get(url=url)
            text = instant.content
            title = instant.title
        except: #InstantParik.DoesNotExist:
            downloaded = trafilatura.fetch_url(url)
            text = trafilatura.extract(downloaded,include_comments=False)
            try:
                metadata = trafilatura.extract_metadata(downloaded)
                title = metadata.title
            except:
                metadata = None
                title = url
            if not text:
                messages.add_message(request, messages.INFO,"Error fetching data")
                return HttpResponseRedirect("/play/instant/")
            try:
                if request.user.is_authenticated:
                    instant = InstantParik(user=request.user,url=url,content=text,description=url,tags="",title=metadata.title)
                else:
                    instant = InstantParik(url=url,content=text,description=url,tags="",title=metadata.title)
                instant.save()
            except:
                pass
        lines = []
        new_lines = text.split(".")
        for line in new_lines:
            new_line = textwrap.wrap(line,width=50)
            lines = lines + new_line

        alldata = []
        for line in lines:
            data = {}
            data['line'] = line
            data['font'] =  'inherit'
            data['color'] = get_random_color()
            alldata.append(data)

        pariks = Parik.objects.all().order_by('-id')
        paginator = Paginator(pariks, 10)  # Show 25 contacts per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

 
        parik ={}
        parik['user'] = request.user
        parik['comments'] = None
        parik['hits'] = None
        parik['font_size'] = "0.6"
        parik['animation'] = {"name":"default"}
        parik['created_on'] = datetime.datetime.now()
        parik['description'] = "Link - " + url
        parik['title'] =  title
        try:
            parik['instant'] = instant
        except:
            pass
        tags = None
        is_subscribed = None
        context = {'instant': True,'parik':parik,'tags':tags,'lines':alldata,'pariks':page_obj,'is_subscribed':is_subscribed,'now':datetime.datetime.now()}
        return render(request, template, context)

@login_required
@page_template('homepage_videos_list.html')  # just add this decorator
def explore(request,extra_context=None,template="explore.html"):
    subscribed_channels = []
    if request.user.is_authenticated:
        subscribed_channels = ChannelSubscriber.objects.filter(subscriber=request.user)

    pariks = Parik.objects.all().order_by('-id')
    paginator = Paginator(pariks, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {'pariks':pariks,'subscribed_channels':subscribed_channels}
    return render(request, template, context)

@login_required
@page_template('homepage_videos_list.html')  # just add this decorator
def subscription(request,extra_context=None,template="subscription.html"):
    subscribed_channels = []
    if request.user.is_authenticated:
        subscribed_channels = ChannelSubscriber.objects.filter(subscriber=request.user)
        users = subscribed_channels.values_list('channel__owner')
    pariks = Parik.objects.filter(user__in=users).order_by('-id')
    paginator = Paginator(pariks, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {'pariks':pariks,'subscribed_channels':subscribed_channels}
    return render(request, template, context)

@login_required
def save_instant(request,id):
    instant = get_object_or_404(InstantParik,id=id)
    animation = Animation.objects.get(pk=1)
    
    if not instant.parik:
        parik = Parik(title=instant.title,user=request.user,content=instant.content,description=instant.description,tags=instant.tags,created_on=datetime.datetime.now(),to_wrap=True,animation=animation,shuffle_colors_by_line=True,shuffle_fonts_by_line=True)
        parik.save()
        instant.is_user_saved = True
        instant.parik = parik
        instant.save()

        message = {'message': 'Post Saved','type':'success','btn_text':'Saved'}
        print(message)
    else:
        message = {'message': 'Already Saved','type':'error','btn_text':'Saved'}

    return HttpResponseRedirect(reverse("single_video", args=[instant.parik.id])) 


