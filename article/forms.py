from django import forms
from mainapp.models import BlogArticleColumn

class BlogArticleColumnForm(forms.ModelForm):
    class Meta:
        model = BlogArticleColumn
        fields = ("column",)

