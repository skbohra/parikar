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
from itertools import chain

DEFAULT_LINE_COLOR = ""
DEFAULT_LINE_FONT = ""

@login_required
def index(request):
    template = "index.html"
    subscribed_channels = []
    if request.user.is_authenticated:
        subscribed_channels = ChannelSubscriber.objects.filter(subscriber=request.user,is_active=True).values('channel__owner')
    print(subscribed_channels)
    pariks = Parik.objects.filter(user__in=subscribed_channels).order_by('-id')
    paginator = Paginator(pariks, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    hitcounts = HitCount.objects.filter(content_type=ContentType.objects.get_for_model(Parik),hits__gte=2)
    
    popular_pariks = Parik.objects.all().order_by('-id')
    paginator = Paginator(popular_pariks, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("popular")
    popular_obj = paginator.get_page(page_number)

    your_instant_pariks = InstantParik.objects.filter(user=request.user,is_user_saved=False).order_by('-id')
    your_pariks = Parik.objects.filter(user=request.user).order_by('-id')
    your_posts  = list(chain(your_instant_pariks, your_pariks))

    paginator = Paginator(your_posts, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("your")
    your_obj = paginator.get_page(page_number)


    context = {'pariks':page_obj,'popular_pariks':popular_obj,'your_pariks':your_obj,'subscribed_channels':subscribed_channels}
    
    return render(request, template, context)

@page_template('videos_list.html')  # just add this decorator
def single_video(request,id=id,extra_context=None,template="play-video.html"):
    try:
        ctype = request.GET['type']
        if ctype == "instant_parik":
            return HttpResponseRedirect(reverse("instant_video")+"?id="+str(id))
    except KeyError:
        pass
    parik = get_object_or_404(Parik,id=id)
    #keywords = extract_keywords_bert(parik.content)
    #print(keywords)
    tags = parik.tags.split(" ")
    if not parik.thumbnail:
        try:
            api_key = ServiceAPI.objects.get(service_name="stability")
            data = stability_text_to_image(parik.title,api_key)
        
            for i, image in enumerate(data["artifacts"]):
                data = ContentFile(base64.b64decode(image["base64"])) 
                uuid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                file_name = api_key.service_name+"_generated_"+ uuid + ".png"
                parik.thumbnail.save(file_name, data, save=True)
        except Exception as e:
            print(e)

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
    paginator = Paginator(pariks, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    record_view_url = reverse("record_post_view", args=[parik.id]) + "?ctype=" + "parik" 
    try:
        view_progress = parik.post_view_stat.get(user=request.user).view_progress
    except:
        view_progress = 0.0
    context = {'parik':parik,'tags':tags,'lines':alldata,'pariks':page_obj,'is_subscribed':is_subscribed,'now':datetime.datetime.now(),'record_view_url':record_view_url,'view_progress':view_progress}
    return render(request, template, context)

@login_required
def add_parik(request):
    form = NewParikForm()
    try:
        request.user.channel
    except Exception as e:
        next_url = reverse("add_parik")
        messages.add_message(request, messages.INFO,"Please update your profile first!")
        return HttpResponseRedirect(reverse("new_channel")+"?next="+next_url) 

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
        except ChannelSubscriber.DoesNotExist as e:
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
    if request.user.is_authenticated:
        try:
            channel = request.user.channel
        except: #User.Channel.DoesNotExist:
            messages.add_message(request, messages.INFO,"Please update your profile first!")
            if url:
                next_url = reverse("instant_video")+"?url="+url
            else:
                next_url = reverse("instant_video")

            return HttpResponseRedirect(reverse("new_channel")+"?next="+next_url) 


    try:
        id = request.GET['id']
    except:
        id = None
    if not url and not id:
        return render(request,'instant-url.html')
    else:

        try:
            if id:
                instant = InstantParik.objects.get(id=id)
                url = instant.url
            else:
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
        record_view_url = reverse("record_post_view", args=[instant.id]) + "?ctype=" + "instant" 
        context = {'instant': True,'parik':parik,'tags':tags,'lines':alldata,'pariks':page_obj,'is_subscribed':is_subscribed,'now':datetime.datetime.now(),'record_view_url':record_view_url}
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


@login_required
def record_post_view(request,id):
    ctype = request.GET['ctype']
    progress = request.GET['progress']
    if ctype == "parik":
        obj = Parik.objects.get(pk=id)
    else:
        obj = InstantParik.objects.get(pk=id)
    try:
        post_view = obj.post_view_stat.get(user=request.user)
        post_view.view_progress = progress
        post_view.save()
    except PostViewStat.DoesNotExist:
        post_view = PostViewStat(content_object=obj,user=request.user,view_progress=progress)
        post_view.save()
    return JsonResponse({"message":"progress_recorded"})

@login_required
def new_channel(request):
    try:
        instance = request.user.channel
        form = NewChannelForm(instance=instance)
    except Exception as e:
        print(e)
        form = NewChannelForm()
        instance = None
    if request.method == "POST":
        if instance:
            form = NewChannelForm(data=request.POST,files=request.FILES,instance=instance)
        else:
            form = NewChannelForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            channel = form.save(commit=False)
            channel.owner = request.user
            channel.created_on = datetime.datetime.now()
            channel.is_active = True
            channel.save()
            messages.add_message(request, messages.SUCCESS,"Profile Updated!")
            if request.GET.get("next"):
                return redirect(request.GET.get('next'))
            else:
                return HttpResponseRedirect("/") 

    context = {'form':form}
    return render(request, "new-channel.html", context)


@login_required
def channels(request):
    channels = Channel.objects.filter(is_active=True)
    context = {"channels":channels}
    return render(request, "channels.html", context)

