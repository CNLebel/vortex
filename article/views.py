from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from mainapp.models import BlogArticleColumn,BlogArticles,Sort,Label
from .forms import BlogArticleColumnForm

import json

# Create your views here.


# 添加栏目
@login_required(login_url='user/login.html')
@csrf_exempt
def blogarticle_column(request):

    if request.method == "GET":
        columns = BlogArticleColumn.objects.all().filter(column_user=request.user)
        column_form = BlogArticleColumnForm()
        userid = request.user.id
        return render(request, "blogarticles/blogarticle_column.html", locals())

    if request.method == "POST":
        column_name = request.POST['column']
        columns = BlogArticleColumn.objects.filter(column_user_id=request.user.id, column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            BlogArticleColumn.objects.create(column_user=request.user, column=column_name)
            return HttpResponse("1")


# 修改栏目
@login_required(login_url='user/login.html')
@require_POST
@csrf_exempt
def edit_blogarticle_column(request):
    column_name = request.POST['column_name']
    column_id = request.POST['column_id']
    try:
        line = BlogArticleColumn.objects.get(column_id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


# 删除栏目
@login_required(login_url='user/login.html')
@require_POST
@csrf_exempt
def del_blogarticle_column(request):
    column_id = request.POST['column_id']
    try:
        line = BlogArticleColumn.objects.get(column_id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")



# 文章标签
@login_required(login_url='user/login.html')
@csrf_exempt
def blogarticle_label(request):
    if request.method == "GET":
        article_label = Label.objects.filter(label_user=request.user)
        return render(request, "blogarticles/blogarticle_label.html", locals())

    if request.method == "POST":
        label_name = request.POST['label']
        labels = Label.objects.filter(label_user_id=request.user.id, label_name=label_name)
        if labels:
            return HttpResponse('2')
        else:
            Label.objects.create(label_user=request.user, label_name=label_name)
            return HttpResponse('1')


# 修改标签
@login_required(login_url='user/login.html')
@require_POST
@csrf_exempt
def edit_blogarticle_label(request):
    label_name = request.POST['label_name']
    label_id = request.POST['label_id']
    try:
        line = Label.objects.get(label_id=label_id)
        line.label_name = label_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


# 删除标签
@login_required(login_url='user/login.html')
@require_POST
@csrf_exempt
def del_blogarticle_label(request):
    label_id = request.POST['label_id']
    try:
        line = Label.objects.get(label_id=label_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


# 发表文章
@login_required(login_url='user/login.html')
@csrf_exempt
def blogarticle_post(request):
    if request.method == "POST":
        article_title = request.POST['article_title']
        article_content = request.POST['article_content']
        column_id = request.POST['column_id']
        sort_id = request.POST['sort_id']
        article_labels = request.POST['article_label']
        abstract = request.POST['abstract']
        abstract_img = request.POST['abstract_img']
        abstract_imgname = abstract_img.split('src=')[1].split('"')[1].split('/')[-1]

        if (article_title != '' and article_content != ''):
            blogarticles=BlogArticles()
            blogarticles.article_title = article_title
            blogarticles.article_content = article_content
            blogarticles.article_author = request.user
            blogarticles.article_column = request.user.article_column.get(column_id=int(column_id))
            blogarticles.article_sort = Sort.objects.get(sort_id=sort_id)
            blogarticles.article_abstract = abstract
            blogarticles.article_abstract_img = abstract_imgname
            blogarticles.save()

            # 添加标签
            if article_labels:
                for label in json.loads(article_labels):
                    lab = request.user.labels.get(label_name=label)
                    blogarticles.article_label.add(lab)

            return HttpResponse("1")
        else:
            return HttpResponse("2")
    else:
        blogarticle_columns = request.user.article_column.all()
        sort = Sort.objects.all()
        article_label = request.user.labels.all()
        return render(request, "blogarticles/blogarticle_post.html",locals())


#文章列表
@login_required(login_url='user/login.html')
@csrf_exempt
def blogarticle_list(request):
    blogarticle_columns = request.user.article_column.all()
    blogarticle = request.user.article_author.all()
    return render(request, 'blogarticles/blogarticle_list.html', locals())


# 删除文章
@login_required(login_url='user/login.html')
@require_POST
@csrf_exempt
def del_blogarticle(request):
    article_id = request.POST['article_id']
    try:
        line = request.user.article_author.get(article_id=article_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


# 编辑文章
@login_required(login_url='user/login.html')
@csrf_exempt
def edit_blogarticle(request,article_id):
    if request.method == "GET":
        blogarticles = request.user.article_author.get(article_id=article_id)
        columns = request.user.article_column.all()
        sorts = Sort.objects.all()
        return render(request, 'blogarticles/edit_blogarticle.html',locals())

    if request.method == "POST":
        article_title = request.POST['article_title']
        article_content = request.POST['article_content']
        column_id = request.POST['column_id']
        sort_id = request.POST['sort_id']
        article_id = request.POST['article_id']

        if (article_title != '' and article_content != ''):
            blogarticles=request.user.article_author.get(article_id=int(article_id))
            blogarticles.article_title = article_title
            blogarticles.article_content = article_content
            blogarticles.article_column = request.user.article_column.get(column_id=int(column_id))
            blogarticles.article_sort = Sort.objects.get(sort_id=int(sort_id))
            blogarticles.save()

            return HttpResponse("1")
        else:
            return HttpResponse("2")