from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from slugify import slugify
from django.urls import reverse

# Create your models here.



#用户数据模型
class MyUser(AbstractUser):
    qq = models.CharField('QQ号码', max_length=20, blank=True, default=' ')
    wechat = models.CharField('微信账号', max_length=20, blank=True, )
    mobile = models.CharField('手机号码', max_length=11, blank=True, default=' ')

    def __str__(self):
        return self.username


#用户详细信息数据模型
class UsersInfo(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, verbose_name='用户')
    user_nickname = models.CharField('用户昵称', max_length=20, blank=True)
    user_profile_photo = models.ImageField('头像',blank=True)
    user_age = models.CharField('出生年月日', max_length=20, blank=True)
    address = models.CharField('联系地址', max_length=200, blank=True)
    occupation = models.CharField('职业', max_length=50, blank=True)
    interest = models.CharField('兴趣爱好', max_length=200, blank=True)
    aboutme = models.TextField('简介', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '用户详细信息'
        verbose_name_plural = '用户详细信息'


#用户好友数据模型
# class UserFriends(models.Model):
# #     uf_id = models.AutoField('序号',primary_key=True)
# #     user_id = models.ForeignKey
# #     user_friends_id = ''
# #     user_note = models.CharField('好友备注',max_length=50)
# #     user_status = models.CharField('好友状态',max_length=50)


# 博客文章栏目数据模型
class BlogArticleColumn(models.Model):
    column_id = models.AutoField('序号', primary_key=True)
    column_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='栏目所属用户', related_name="article_column")
    column = models.CharField('栏目', max_length=200, blank=True)
    created = models.DateField('创建日期', auto_now_add=True)

    def __str__(self):
        return self.column

    class Meta:
        verbose_name = '文章栏目'
        verbose_name_plural = '文章栏目'


#博客文章分类的数据模型
class Sort(models.Model):
    sort_id = models.AutoField('序号', primary_key=True)
    sort_name = models.CharField('分类名称', max_length=50, blank=True)
    sort_alias = models.CharField('分类别名', max_length=50, blank=True)
    sort_description = models.TextField('分类描述', blank=True)
    parent_sort_id = models.IntegerField('父分类ID', default=0, blank=True)

    def __str__(self):
        return self.sort_name

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = '文章分类'


#博客文章标签数据模型
class Label(models.Model):
    label_id = models.AutoField('序号', primary_key=True)
    label_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='标签所属用户', related_name="labels")
    label_name = models.CharField('标签名称', max_length=500, blank=True)
    label_alias = models.CharField('标签别名', max_length=500, blank=True)
    label_description = models.TextField('标签描述', blank=True)

    def __str__(self):
        return self.label_name

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = '文章标签'


#博客文章主要的数据模型
class BlogArticles(models.Model):
    article_id = models.AutoField('序号',primary_key=True)
    article_author = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='文章作者', related_name='article_author')
    article_title = models.CharField('博文标题', max_length=200, blank=True)
    article_slug = models.CharField('博文链接', max_length=500, blank=True)
    article_content = models.TextField('博文内容', blank=True)
    article_abstract = models.CharField('摘要',max_length=500, blank=True)
    article_abstract_img = models.ImageField('摘要图片',blank=True)
    article_views = models.IntegerField('浏览量', default=0, blank=True)
    article_comment_count = models.IntegerField('评论总数', default=0)
    article_date = models.DateTimeField('发表时间',default=timezone.now())
    article_update = models.DateTimeField('编辑时间', auto_now=True)
    article_like_count = models.IntegerField('点赞数', default=0, blank=True)
    article_like = models.ManyToManyField(MyUser, verbose_name='点赞', related_name='articles_like', blank=True)
    article_column = models.ForeignKey(BlogArticleColumn, on_delete=models.CASCADE, verbose_name='所属栏目',related_name="article_column")
    article_sort = models.ForeignKey(Sort, on_delete=models.CASCADE, verbose_name='文章分类', blank=True, related_name="article_sort")
    article_label = models.ManyToManyField(Label, verbose_name='文章标签', related_name='article_label', blank=True)

    def __str__(self):
        return self.article_title

    class Meta:
        ordering = ("article_title",)
        index_together = (('article_id','article_slug'),)
        verbose_name = '博客文章'
        verbose_name_plural = '博客文章'

    def save(self, *args, **kwargs):
        self.article_slug = slugify(self.article_title)
        super(BlogArticles, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blogarticle_detall",args=[self.article_id, self.article_slug])




#评论的数据模型
class Comment(models.Model):
    comment_id = models.AutoField('序号', primary_key=True)
    comment_article = models.ForeignKey(BlogArticles, on_delete=models.CASCADE, verbose_name='评论文章')
    comment_commentator = models.CharField('评论用户', max_length=90, blank=True)
    comment_date = models.DateTimeField('评论时间', default=timezone.now())
    comment_content = models.TextField('评论内容', blank=True)
    parent_comment_id = models.IntegerField('父评论ID', default=0, blank=True)
    # comment_like_count = models.IntegerField('点赞数', default=0, blank=True)
    #
    # def __str__(self):
    #     return "Comment by {0} on {1}".format(self.comment_commentator.username, self.comment_article)

    class Meta:
        verbose_name = '博文评论'
        verbose_name_plural = '博文评论'



