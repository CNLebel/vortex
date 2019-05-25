from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Label)
admin.site.register(Sort)
admin.site.register(BlogArticles)
admin.site.register(Comment)
admin.site.register(BlogArticleColumn)