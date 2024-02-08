import asyncio
import hashlib
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from movie.getfilmdescription import getfilmdescription, getSeriesMessage, getplaym3u8
from . import consumers
from .models import Video
from .search2api import query2
from .utils import random_str, str2md5

SEARCH_CACHE = {}


# Create your views here.

def search_page(request):
    return render(request, 'search.html')


def search_page2(request):
    return render(request, 'search2.html')


def movie_page(request):
    query = request.GET.get('query')
    usedb = request.GET.get('usedb', True) != 'false'

    # 检查缓存
    if SEARCH_CACHE.get(query) and usedb:
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
                    temp = Video.objects.filter(now=item['now'])
                    if not temp:  # m3u8地址不重复
                        Video.objects.create(**item)
    return render(request, 'movie.html', {
        "movies": data,
        "query": query,
        "count": len(data)
    })


def movie_page2(request):
    query = request.GET.get('query')
    page = request.GET.get('page', 1)
    movies = query2(query, page)
    return render(request, 'movie2.html', {
        "movies": movies,
        "query": query,
        "page": page,
        "next_page": int(page) + 1,
        "prev_page": int(page) - 1
    })


TOKEN_CACHE = {}


def get_live(request):
    m3u8Url = request.GET.get('url', None)
    playpage = request.GET.get('playpage', None)
    image = request.GET.get('image', None)
    title = request.GET.get('title', None)
    if not m3u8Url and not playpage:
        return HttpResponse("没有可以播放的地址")

    # 生成随机str
    _str = random_str(8)
    # 形成md5字符串
    if not m3u8Url:
        # 没有m3u8地址, 从playpage中爬取
        m3u8Url, _ = getplaym3u8(playpage)
    token = _str + "_" + str2md5(m3u8Url)
    if TOKEN_CACHE.get(token):
        # token已经存在, 重新生成一个不重复的token
        return get_live(request)
    # 获取集数信息
    series = None
    if playpage:
        series = getSeriesMessage(playpage)  # 集数信息

    TOKEN_CACHE[token] = {"m3u8Url": m3u8Url, "token": token, "series": series, "image": image, "title": title}

    return render(request, 'live.html', TOKEN_CACHE[token])


def live_stream(request, token=None):
    if not token:
        return HttpResponse("token is required")
    token_item = TOKEN_CACHE.get(token)
    if not token_item:
        return HttpResponse("房间不存在")
    m3u8Url = token_item.get('m3u8Url')
    return render(request, 'share.html', {"m3u8Url": m3u8Url, "token": token})


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


def get_rooms(request):
    """
    获取房间列表
    :param request:
    :return:
    """
    data = consumers.ROOM_CACHE
    res = []
    # 把data中所有对象转为dict
    for token in data:
        obj = {
            'token': token,
            'count': len(data[token]),
            'title': TOKEN_CACHE[token].get('title'),
            'image': TOKEN_CACHE[token].get('image'),
            'users': []
        }
        for i in range(len(data[token])):
            ip, port = data[token][i].__dict__['scope']['client']
            obj['users'].append({'ip': ip, 'port': port})
        res.append(obj)
    return render(request, 'rooms.html', {'rooms': res})
