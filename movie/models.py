from django.db import models

# Create your models here.
from django.db import models
from django.utils.html import format_html


class Video(models.Model):
    image = models.CharField(max_length=500, verbose_name="封面图片", blank=True, null=True)
    title = models.CharField(max_length=100, verbose_name="视频标题", blank=True, null=True)
    director = models.CharField(max_length=50, verbose_name="导演", blank=True, null=True)
    actor = models.TextField(verbose_name="演员", blank=True, null=True)
    type = models.CharField(max_length=255, verbose_name="节目类型", blank=True, null=True)
    area = models.CharField(max_length=255, verbose_name="地区", blank=True, null=True)
    time = models.CharField(max_length=255, verbose_name="发行年份",
                            help_text="例如：大陆年份：2009，建议拆分为两个字段：地区和年份", blank=True, null=True)
    playpage = models.CharField(max_length=500, verbose_name="播放页面URL", blank=True, null=True)
    now = models.CharField(max_length=500, verbose_name="当前集数播放地址(m3u8)", blank=True, null=True)
    next = models.CharField(max_length=500, verbose_name="下一集播放地址", blank=True, null=True)

    def img_preview(self):
        return format_html('<img src="{}" width="100px"/>', self.image)

    def play_button(self):
        btn_str = '<a href="{}" target="_blank">播放</a>'
        return format_html(btn_str, '/live?url=' + self.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    # def __dict__(self):
    #     return {
    #         "image": self.image,
    #         "title": self.title,
    #         "director": self.director,
    #         "actor": self.actor,
    #         "type": self.type,
    #         "area": self.area,
    #         "time": self.time,
    #         "playpage": self.playpage,
    #         "now": self.now,
    #         "next": self.next,
    #     }
