from django.shortcuts import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import textwrap
from .models import * 
from .forms import * 
import datetime 

def index(request):
    pariks = Parik.objects.all().order_by('-id')
    context = {'pariks':pariks}
    return render(request, "index.html", context)


def single_video(request,id):
    parik = get_object_or_404(Parik,id=id)
    tags = parik.tags.split(" ")
    if parik.to_wrap:
        lines = textwrap.wrap(parik.content,width=50)
    else:
        lines = parik.content.split("\n")
    pariks = Parik.objects.all().exclude(id=id).order_by('-id')
    context = {'parik':parik,'tags':tags,'lines':lines,'pariks':pariks}
    return render(request, "play-video.html", context)


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



def search(request):
    term = request.GET['query']
    pariks = Parik.objects.filter(title__contains=term)
    context = {'pariks':pariks}
    return render(request, "search.html", context)


