from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse

# Register your models here.

from movie.models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    search_fields = ['title', 'director', 'actor', 'type', 'area', 'time']
    # actions = ['play']
    list_display = ['img_preview', 'title', 'director', 'actor', 'type', 'area', 'time', 'play_button']

    # def play(self, request, queryset):
    #     # 跳转到播放地址
    #     return HttpResponse(f"<script>window.open('{queryset[0].now}')</script>")
