from django.shortcuts import render, redirect, HttpResponse
from mainapp.models import *
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from .forms import MyUserCreationForm
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import json
import random
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
import hashlib




# Create your views here.


# 创建验证码ajax刷新验证码时调用
def captcha():
    hashkey = CaptchaStore.generate_key()    # 验证码
    image_url = captcha_image_url(hashkey)     # 验证码地址
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha

# 刷新验证码调用前面定义的(captcha创建验证码)
def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')

# 验证验证码
def jarge_captcha(captchaStr, captchaHashkey):
    if captchaStr and captchaHashkey:
        try:
            # 获取根据hashkey获取数据库中的response值
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
            # 如果验证码匹配
            if get_captcha.response == captchaStr.lower():
                return True
        except:
            return False
    else:
        return False



#用户的注册和登录
def loginView(request):
    # 表单对象user
    user = MyUserCreationForm()

    # 验证码，第一次请求向页面发送验证码
    hashkey = CaptchaStore.generate_key()  # 验证码
    image_url = captcha_image_url(hashkey)  # 验证码地址
    captcha = {'hashkey': hashkey, 'image_url': image_url}

    # 表单提交
    if request.method == 'POST':
        # 判断表单提交是用户登录还是用户注册
        # 用户登录
        if request.POST.get('loginUser', ''):
            loginUser = request.POST.get('loginUser', '')
            password = request.POST.get('password', '')
            capt = request.POST.get('captcha', '')
            key = request.POST.get('hashkey', '')
            # 调用前面定义的jarge_captcha函数进行验证
            if jarge_captcha(capt,key):
                if MyUser.objects.filter(Q(mobile=loginUser) | Q(username=loginUser)):
                    user = MyUser.objects.filter(Q(mobile=loginUser) | Q(username=loginUser)).first()
                    if check_password(password, user.password):
                        login(request, user)
                        if not UsersInfo.objects.filter(user=request.user):
                            UsersInfo.objects.create(user=request.user)
                        return redirect('/index')
                    else:
                        tips = '密码错误'
                else:
                    tips = '用户不存在'
            else:
                tips = '验证码错误'

        # 用户注册
        else:
            user = MyUserCreationForm(request.POST)
            capt = request.POST.get('captcha', '')
            key = request.POST.get('hashkey', '')
            # 调用前面定义的jarge_captcha函数进行验证
            if jarge_captcha(capt, key):
                if user.is_valid():
                    user.save()
                    tips = '注册成功'
                    return redirect('/user/login.html')
                else:
                    if user.errors.get('username',''):
                        tips = user.errors.get('username', '注册失败')
                    else:
                        tips = user.errors.get('mobile', '注册失败')
            else:
                tips = '验证码错误'

    return render(request, 'user/login.html', locals())


# 退出登录
def logoutView(request):
    logout(request)
    return redirect('login.html')


# 修改密码
def setpasswordView(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        old_password = request.POST.get('password', '')
        new_password = request.POST.get('new_password', '')
        # 判断用户是否存在
        if MyUser.objects.filter(Q(mobile=username) | Q(username=username)):
            user = authenticate(username=username, password=old_password)
            if user:
                # 密码加密处理并保存到数据库
                dj_ps = make_password(new_password, None, 'pbkdf2_sha256')
                user.password = dj_ps
                user.save()
                response_message='密码修改成功!'
            else:
                redirect('setpassword')

    return render(request, 'user/setpassword.html', locals())


# 找回密码
def findPassword(request):
    button = '获取验证码'
    new_password = False
    if request.method == 'POST':
        username = request.POST.get('username', 'root')
        VerificationCode = request.POST.get('VerificationCode', '')
        password = request.POST.get('password', '')
        user=MyUser.objects.filter(Q(mobile=username) | Q(username=username))
        if not user:
            tips = '用户' + username + '不存在'
        else:
            #判断验证码是否已发送
            if not request.session.get('VerificationCode', ''):
                # 发送验证码并将验证码写入
                button = '重置密码'
                tips = '验证码已发送'
                new_password = True
                VerificationCode = str(random.randint(1000,9999))
                request.session['VerificationCode'] = VerificationCode
                user[0].email_user('找回密码', VerificationCode)
                print(VerificationCode)
            # 匹配输入的验证码是否正确
            elif VerificationCode == request.session.get('VerificationCode'):
                #密码加密处理并保存到数据库
                dj_ps = make_password(password, None, 'pbkdf2_sha256')
                user[0].password = dj_ps
                user[0].save()
                del request.session['VerificationCode']
                tips = '密码已重置'
            # 输入验证码错误
            else:
                tips = '验证错误，请重新获取'
                new_password = False
                del request.session['VerificationCode']
    return render(request, 'user/findpassword.html', locals())

@login_required(login_url='user/login.html')
@csrf_exempt
def userinfo(request):
    userinfo = UsersInfo.objects.get(user=request.user)
    return render(request, 'user/userinfo.html',locals())


@login_required(login_url='user/login.html')
@csrf_exempt
def edit_userinfo(request):
    if request.method == 'POST':
        user_nickname = request.POST['user_nickname']
        user_age = request.POST['user_age']
        address = request.POST['address']
        occupation = request.POST['occupation']
        interest = request.POST['interest']
        aboutme = request.POST['aboutme']

        if request.user:
            userinfo = UsersInfo.objects.get(user=request.user)
            userinfo.user_nickname = user_nickname
            userinfo.user_age = user_age
            userinfo.address = address
            userinfo.occupation = occupation
            userinfo.interest = interest
            userinfo.aboutme = aboutme
            userinfo.save()
            return HttpResponse("1")

    else:
        userinfo = UsersInfo.objects.get(user=request.user)
        return render(request, 'user/edit_userinfo.html',locals())


@login_required(login_url='user/login.html')
@csrf_exempt
def picture_upload(request):
    if request.method == 'POST':
        imagefile=request.FILES['file']
        if imagefile:
            time_now = timezone.now()  # 获取当前日期时间
            m = hashlib.md5()
            m.update(str(time_now).encode())  # 给当前时间编码
            time_now = m.hexdigest()

            filename = time_now + '.png'
            path = str(settings.MEDIA_ROOT).strip("[,],',")[1:]
            with open(path+filename, 'wb+') as destination:
                for chunk in imagefile.chunks():
                    destination.write(chunk)
            userinfo = UsersInfo.objects.get(user=request.user)
            userinfo.user_profile_photo = filename
            userinfo.save()
            return HttpResponse('1')
        else:
            return HttpResponse('2')
    else:
        return render(request, 'user/picture_upload.html',locals())

