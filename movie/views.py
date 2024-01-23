import asyncio
import hashlib
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from movie.getfilmdescription import getfilmdescription
from .models import Video
from .utils import random_str, str2md5

VIDEO_ROOMS_CACHE = {}
SEARCH_CACHE = {}


# Create your views here.

def search_page(request):
    return render(request, 'search.html')


def movie_page(request):
    query = request.GET.get('query')
    usedb = request.GET.get('usedb', True) != 'false'

    # 检查缓存
    if SEARCH_CACHE.get(query):
        data = SEARCH_CACHE.get(query)
    else:
        video = Video.objects.filter(title__contains=query)
        if video and usedb:  # 检查数据库有没有
            data = [item.__dict__ for item in video]
        else:
            data = getfilmdescription(query)
            SEARCH_CACHE[query] = data
            # 没检索过
            if not video:
                for item in data:
                    Video.objects.create(**item)
    return render(request, 'movie.html', {
        "movies": data
    })


TOKEN_CACHE = {}


def get_live(request):
    m3u8Url = request.GET.get('url')
    # 生成随机str
    _str = random_str(8)
    # 形成md5字符串
    token = _str + "_" + str2md5(m3u8Url)

    if TOKEN_CACHE.get(token):
        # token已经存在
        return get_live(request)

    TOKEN_CACHE[token] = {"m3u8Url": m3u8Url, "token": token}

    return render(request, 'live.html', TOKEN_CACHE[token])


def live_stream(request, token=None):
    if not token:
        return HttpResponse("token is required")
    token_item = TOKEN_CACHE.get(token)
    if not token_item:
        return HttpResponse("房间不存在")
    m3u8Url = token_item.get('m3u8Url')
    return render(request, 'share.html', {"m3u8Url": m3u8Url, "token": token})


# PROGRESS_CACHE = {"currentTime": 388.649582, "duration": 1379.7866670000003, "status": "play"}
PROGRESS_CACHE = {
    "token": {"currentTime": 388.649582, "duration": 1379.7866670000003, "status": "play"},
}


def set_progress(request):
    token = request.GET.get('token')
    if not token:
        return HttpResponse("token is required")

    if request.method == "POST":
        data = json.loads(request.body)
        PROGRESS_CACHE[token] = data
    return JsonResponse(PROGRESS_CACHE.get(token))


indexx = 0


# 把ts文件过渡传输
def ts_stream(request):
    global indexx
    # 重复播放

    res = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-ALLOW-CACHE:YES
#EXT-X-MEDIA-SEQUENCE:{indexx}
#EXT-X-PLAYLIST-TYPE:EVENT
#EXT-X-KEY:METHOD=AES-128,URI="https://v.gsuus.com/play/7ax76GBe/enc.key"
#EXTINF:5.000000,
https://gs.gszyi.com:999/hls/46/20230114/946812/plist-00001.ts
#EXTINF:5.000000,
"""
    indexx = indexx + 1
    return HttpResponse(res, content_type='application/octet-stream')
