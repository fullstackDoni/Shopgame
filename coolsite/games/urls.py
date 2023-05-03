from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
         path('', (GamesHome.as_view()), name='home'),
         path('about/', about, name='about'),
         path('addpage/', addpage, name='add_page'),
         path('contact/', contact, name='contact'),
         path('login/', LoginUser.as_view(), name='login'),
         path('logout/', logout_user, name='logout'),
         path('register/', RegisterUser.as_view(), name='register'),
         path('games/<slug:games_slug>/', ShowGames.as_view(), name='games'),
         path('category/<slug:cat_slug>/', GamesCategory.as_view(), name='category'),
]
