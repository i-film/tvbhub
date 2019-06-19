import datetime

from django.conf import settings
from django.db import models

from videos.models import Video


class CommentQuerySet(models.query.QuerySet):

    def get_count(self):
        return self.count()

    def get_today_count(self):
        return self.exclude(timestamp__lt=datetime.date.today()).count()


class Comment(models.Model):
    list_display = ('content', 'timestamp',)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.CharField(max_length=100, blank=True, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CommentQuerySet.as_manager()

    class Meta:
        db_table = 'COMMENTS'
