from django.db import models


class UserInfo(models.Model):
    user = models.CharField(max_length=64,db_index=True)
    email = models.CharField(max_length=64,unique=True)
    pwd = models.CharField(max_length=64)
    ctime = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=("user","email")


class SendMsg(models.Model):
    code = models.CharField(max_length=4)
    email = models.CharField(max_length=64,unique=True)
    last_time = models.DateTimeField()
    times = models.IntegerField(max_length=2)


class News(models.Model):
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=128,null=True)
    url = models.URLField(max_length=128)
    user = models.ForeignKey(to="UserInfo",related_name="ui",on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    news_type_choice = (
        (1,"42区"),
        (2,"段子"),
        (3,"图片"),
        (4,"挨踢1024"),
    )
    news_type = models.IntegerField(choices=news_type_choice)
    favor_count = models.CharField(max_length=64,default=0)
    comment_count = models.CharField(max_length=64,default=0)


class Comment(models.Model):
    user = models.ManyToManyField(to="UserInfo")
    news = models.ForeignKey(to="News",on_delete=models.CASCADE)
    content = models.CharField(max_length=128)
    device = models.CharField(max_length=64)
    parent_comment = models.ForeignKey(to="self",on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)