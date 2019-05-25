from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from PIL import Image
import json
import os
from time import time
from django.utils import timezone
import hashlib


from django.conf import settings

from .models import BlogArticleColumn,BlogArticles,Sort,Label
from .forms import BlogArticleColumnForm
# Create your views here.

def index(request):
    newests = BlogArticles.objects.all().order_by("-article_views").all()[:4]
    praisemosts = BlogArticles.objects.all().order_by("-article_like_count").all()[:5]
    return render(request, 'index.html',locals())


def technology(request):
    return render(request, 'mainapp/technology.html', locals())


def sentiment(request):
    newests = BlogArticles.objects.filter(article_sort__sort_name="生活感言").order_by("-article_date").all()[:8]
    hottests = BlogArticles.objects.filter(article_sort__sort_name="生活感言").order_by("-article_views").all()[:6]
    return render(request, 'mainapp/sentiment.html', locals())


def recollections(request):
    newests = BlogArticles.objects.filter(article_sort__sort_name="读书感言").order_by("-article_date").all()[:8]
    hottests = BlogArticles.objects.filter(article_sort__sort_name="读书感言").order_by("-article_views").all()[:6]
    return render(request, 'mainapp/recollections.html', locals())


@csrf_exempt
def about(request):
    if request.method == "POST":
        feedback_content = request.POST['feedback_content']
        feedback_contact = request.POST['feedback_contact']
        hah = ' ' + ',' + ' '
        with open("feedback.txt","a+") as feedback:
            # feedback.write("邮件&称呼:" + feedback_contact + "\t" + ","  + "反馈内容:" + feedback_content+"\n")
            feedback.write("邮件&称呼:{0}{1}反馈内容:{2}\n".format(feedback_contact,hah,feedback_content))
        return HttpResponse("1")
    else:
        return render(request, 'mainapp/about.html', locals())


def detail(request,id):
    blogarticle = BlogArticles.objects.filter(article_id=int(id))[0]
    return render(request, 'mainapp/detailsarticle.html', locals())












