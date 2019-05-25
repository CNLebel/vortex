from django.urls import path,re_path
from . import views



urlpatterns = [
    path('index',views.index, name='index'),
    path('',views.index, name='index'),
    path('sentiment', views.sentiment, name='sentiment'),
    path('about', views.about, name='about'),
    path('recollections', views.recollections, name='recollections'),
    path('technology', views.technology, name='technology'),
    re_path('detail/(\d*)/$', views.detail, name='detail'),

]