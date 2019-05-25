from django.urls import path, re_path
from . import views

urlpatterns= [
    path('blogarticle_column', views.blogarticle_column, name='blogarticle_column'),
    path('edit_blogarticle_column', views.edit_blogarticle_column, name='edit_blogarticle_column'),
    path('del_blogarticle_column', views.del_blogarticle_column, name='del_blogarticle_column'),

    path('blogarticle_label', views.blogarticle_label, name='blogarticle_label'),
    path('edit_blogarticle_label', views.edit_blogarticle_label, name='edit_blogarticle_label'),
    path('del_blogarticle_label', views.del_blogarticle_label, name='del_blogarticle_label'),

    path('blogarticle_post',views.blogarticle_post, name='blogarticle_post'),
    path('blogarticle_list', views.blogarticle_list, name='blogarticle_list'),
    path('del_blogarticle', views.del_blogarticle, name='del_blogarticle'),
    re_path(r'^edit_blogarticle/(\d*)/$', views.edit_blogarticle, name='edit_blogarticle'),

]
