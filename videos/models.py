import os

from django.conf import settings
from django.db import models
from django.dispatch import receiver


class VideoQuerySet(models.query.QuerySet):
    def get_count(self):
        return self.count()

    def get_published_count(self):
        return self.filter(status=0).count()

    def get_not_published_count(self):
        return self.filter(status=1).count()

    def get_published_list(self):
        return self.filter(status=0).order_by('-create_time')

    def get_search_list(self, q):
        if q:
            return self.filter(title__contains=q).order_by('-create_time')
        else:
            return self.order_by('-create_time')

    def get_recommend_list(self):
        return self.filter(status=0).order_by('-view_count')[:3]  # 推荐前3条观看最多的视频


class Classification(models.Model):
    """
    分类表
    字段有title(分类名称)和status(是否启用)
    """

    list_display = ('title',)
    title = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'CLASSIFICATIONS'


class Video(models.Model):
    """
    classification是一个ForeignKey外键字段，表示一个分类对应多个视频，一个视频对应一个分类(多对一)
    """

    STATUS_CHOICES = (
        ('0', '发布中'),
        ('1', '未发布'),
    )
    title = models.CharField(max_length=50, blank=True, null=True)
    desc = models.CharField(max_length=100, blank=True, null=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, null=True)
    file = models.FileField(max_length=256)
    cover = models.ImageField(upload_to='cover/', blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True, null=True)
    view_count = models.IntegerField(default=0, blank=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_videos')  # 喜欢的用户
    create_time = models.DateTimeField(auto_now_add=True, blank=True, max_length=20)

    objects = VideoQuerySet.as_manager()

    class Meta:
        db_table = 'VIDEOS'

    def increase_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def switch_like(self, user):
        if user in self.liked.all():
            self.liked.remove(user)
        else:
            self.liked.add(user)

    def count_likers(self):
        return self.liked.count()

    def user_liked(self, user):
        if user in self.liked.all():
            return 0
        else:
            return 1


@receiver(models.signals.post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    删除FileField文件
    """

    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
