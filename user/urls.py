from django.urls import path
from . import views

urlpatterns = [
    #用户的注册和登录
    path('login.html', views.loginView, name='login'),
    # 退出用户登录
    path('logout.html', views.logoutView, name='logout'),
    path('setpassword.html', views.setpasswordView, name='setpassword'),
    path('findpassword.html', views.findPassword, name='findPassword'),

    # 刷新验证码，ajax
    path('refresh_captcha/', views.refresh_captcha, name='refresh_captcha'),

    #用户中心
    path('userinfo',views.userinfo, name='userinfo'),
    path('edit_userinfo',views.edit_userinfo, name='edit_userinfo'),
    path('picture_upload',views.picture_upload, name='picture_upload'),

]
