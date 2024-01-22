from django.db import models

# Create your models here.
from django.db import models


class Video(models.Model):
    image = models.URLField(max_length=500, verbose_name="封面图片")
    title = models.CharField(max_length=100, verbose_name="视频标题")
    director = models.CharField(max_length=50, verbose_name="导演")
    actor = models.TextField(verbose_name="演员", blank=True)
    type = models.CharField(max_length=50, verbose_name="节目类型")
    area = models.CharField(max_length=50, verbose_name="地区")
    time = models.CharField(max_length=50, verbose_name="发行年份",
                            help_text="例如：大陆年份：2009，建议拆分为两个字段：地区和年份")
    playpage = models.URLField(max_length=500, verbose_name="播放页面URL", blank=True)
    now = models.URLField(max_length=500, verbose_name="当前集数播放地址(m3u8)")
    next = models.URLField(max_length=500, verbose_name="下一集播放地址", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __dict__(self):
        return {
            "image": self.image,
            "title": self.title,
            "director": self.director,
            "actor": self.actor,
            "type": self.type,
            "area": self.area,
            "time": self.time,
            "playpage": self.playpage,
            "now": self.now,
            "next": self.next,
        }