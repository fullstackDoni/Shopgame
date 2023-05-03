from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить игру", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


def index(request):
    games = Games.objects.all()

    context = {
        'games': games,

        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }

    return render(request, 'games/index.html', context=context)


def about(request):
    return render(request, 'games/about.html', {'menu': menu, 'title': 'О сайте'})


def addpage(request):
    if request.method == 'POST':
        form = AddGameForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            try:
                Games.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')

    else:
        form = AddGameForm()
    return render(request, 'games/addpage.html', {'form': form, 'menu': menu, 'title': ''})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def show_games(request, games_slug):
    games = get_object_or_404(Games, slug=games_slug)

    context = {
        'games': games,
        'menu': menu,
        'title': games.title,
        'cat_selected': games.cat_id,
    }

    return render(request, 'games/games.html', context=context)


def show_category(request, cat_id):
    games = Games.objects.filter(cat_id=cat_id)

    if len(games) == 0:
        raise Http404()

    context = {
        'games': games,
        'menu': menu,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat_id,
    }

    return render(request, 'games/index.html', context=context)
