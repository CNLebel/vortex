from django import forms
from .models import BlogArticleColumn, BlogArticles

class BlogArticleColumnForm(forms.ModelForm):
    class Meta:
        model = BlogArticleColumn
        fields = ("column",)

