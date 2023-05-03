from coolsite import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from games.views import *
from django.urls import path, include
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'games', GamesViewSet)

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