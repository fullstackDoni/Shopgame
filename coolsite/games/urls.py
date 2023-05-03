from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', GamesHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', addpage, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('games/<slug:games_slug>/', ShowGames.as_view(), name='games'),
    path('category/<slug:cat_slug>/', GamesCategory.as_view(), name='category'),
]
