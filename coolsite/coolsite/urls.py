from coolsite import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from games.views import *
from django.urls import path, include
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('captcha', include('captcha.urls')),
    path('', include('games.urls')),
    path('api/v1/games/', GamesAPIList.as_view()),
    path('api/v1/games/<int:pk>/', GamesAPIUpdate.as_view()),
    path('api/v1/gamesdelete/<int:pk>/', GamesAPIDestroy.as_view()),
    path('api/v1/auth/', include('djoser.urls')),  # new
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # new
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
