from django.shortcuts import render

VIDEO_ROOMS_CACHE = {}


# Create your views here.

def search_page(request):
    return render(request, 'search.html')


def movie_page(request):
    return render(request, 'movie.html', {
        "movies": [{
            'poster_url': "https://t13.baidu.com/it/u=1340163082,2176028497&fm=58&app=83&size=w931&n=0&f=JPEG&fmt=auto?sec=1705683600&t=8d9b9a9e2b8e8bd272e7c1ff04a348d4",
            'title': "我和我的家乡",
            'rate': "8.7",
            'director': "宁浩",
            'genre': "剧情",
            'release_year': "2020",
        }]
    })


def get_live(request):
    return render(request, 'live.html')
