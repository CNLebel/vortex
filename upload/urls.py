from django.urls import path
from . import views

urlpatterns = [

    path('upload_img',views.upload_img, name='upload_img'),
]

