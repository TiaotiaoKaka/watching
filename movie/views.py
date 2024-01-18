import hashlib
import json

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from movie.getfilmdescription import getfilmdescription

VIDEO_ROOMS_CACHE = {}
SEARCH_CACHE = {}


# Create your views here.

def search_page(request):
    return render(request, 'search.html')


def movie_page(request):
    query = request.GET.get('query')
    if SEARCH_CACHE.get(query):
        data = SEARCH_CACHE.get(query)
    else:
        data = getfilmdescription(query)
        SEARCH_CACHE[query] = data
    return render(request, 'movie.html', {
        "movies": data
    })


TOKEN_CACHE = {}


def get_live(request):
    m3u8Url = request.GET.get('url')
    # 形成md5字符串
    md5 = hashlib.md5().hexdigest()
    # 生成随机str
    TOKEN_CACHE[md5] = {"m3u8Url": m3u8Url}

    return render(request, 'live.html', {"token": md5, "m3u8Url": m3u8Url})


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


# 把ts文件过渡传输
def ts_stream(request):
    url = request.GET.get('url')
    res = requests.get(url)
    return HttpResponse(res.content, content_type='application/octet-stream')
