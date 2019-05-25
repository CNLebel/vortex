from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect

from django.utils import timezone
from django.conf import settings

from PIL import Image
import hashlib
import json


# Create your views here.


# 上传图片处理
@login_required(login_url='user/login.html')
@require_POST
@csrf_exempt
def upload_img(request):
    try:
        file = request.FILES.get('file')
        time_now = timezone.now()     #获取当前日期时间
        m = hashlib.md5()
        m.update(str(time_now).encode())    #给当前时间编码
        time_now = m.hexdigest()

        # send_path = os.path.join(settings.MEDIA_ROOT,'image/' + time_now + file.name)
        # send_path = str(settings.MEDIA_ROOT).strip("[,],',") + 'image/'    #上传文件本地保存路径
        send_name = (time_now + file.name)     #上传文件本地保存文件名

        img = Image.open(file)
        img.thumbnail((500, 500), Image.ANTIALIAS)
        try:
            img.save('/home/litong/Projects/PyCharm/vortex/static/media/' + send_name)

            print("img save pass")
        except:
            print("img.save error")

        path = str(settings.MEDIA_ROOT).strip("[,],',") + send_name
        print(path)
        return HttpResponse(json.dumps({'location':path}))

    except Exception:
        return HttpResponse("error")


