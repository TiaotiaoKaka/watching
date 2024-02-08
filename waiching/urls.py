"""
URL configuration for waiching project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import movie.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movie.views.search_page),
    path('search2', movie.views.search_page2),
    path('movie', movie.views.movie_page),
    path('movie2', movie.views.movie_page2),
    path('live', movie.views.get_live),
    # path('streaming', movie.views.live_stream),
    path('streaming/<str:token>', movie.views.live_stream),
    path('progress', movie.views.set_progress),
    path('tsreaming', movie.views.ts_stream),
    path('rooms', movie.views.get_rooms),
    path('hot', movie.views.hot_movie_page),
]
