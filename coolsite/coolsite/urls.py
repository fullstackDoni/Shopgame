from coolsite import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from games.views import *
from django.urls import path, include
from rest_framework import routers


class MyCustomRouter(routers.SimpleRouter):
    routes = [
        routers.Route(url=r'^{prefix}$',
                      mapping={'get': 'list'},
                      name='{basename}-list',
                      detail=False,
                      initkwargs={'suffix': 'List'}),
        routers.Route(url=r'^{prefix}/{lookup}$',
                      mapping={'get': 'retrieve'},
                      name='{basename}-detail',
                      detail=True,
                      initkwargs={'suffix': 'Detail'})
    ]


router = MyCustomRouter()
router.register(r'games', GamesViewSet, basename='women')
print(router.urls)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha', include('captcha.urls')),
    path('', include('games.urls')),
    path('api/v1/', include(router.urls)),
    # path('api/v1/gameslist', GamesViewSet.as_view({'get': 'list'})),
    # path('api/v1/gameslist/<int:pk>/', GamesViewSet.as_view({'put': 'update'})),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
