from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from .forms import *
from .models import *
from .serializers import GameSerializer
from .utils import *
from rest_framework import generics

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить игру", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}]


class GamesHome(DataMixin, ListView):
    model = Games
    template_name = 'games/index.html'
    context_object_name = 'games'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Games.objects.filter(is_published=True).select_related('cat')


# def index(request):
#     games = Games.objects.all()
#
#     context = {
#         'games': games,
#
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'games/index.html', context=context)


def about(request):
    contact_list = Games.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'games/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


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


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'games/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# def show_games(request, games_slug):
#     games = get_object_or_404(Games, slug=games_slug)
#
#     context = {
#         'games': games,
#         'menu': menu,
#         'title': games.title,
#         'cat_selected': games.cat_id,
#     }
#
#     return render(request, 'games/games.html', context=context)


class AddGames(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddGameForm
    template_name = 'games/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление игры")
        return dict(list(context.items()) + list(c_def.items()))


class ShowGames(DataMixin, DetailView):
    model = Games
    template_name = 'games/games.html'
    slug_url_kwarg = 'games_slug'
    context_object_name = 'games'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['games'])
        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, cat_id):
#     games = Games.objects.filter(cat_id=cat_id)
#
#     if len(games) == 0:
#         raise Http404()
#
#     context = {
#         'games': games,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_id,
#     }
#
#     return render(request, 'games/index.html', context=context)

class GamesCategory(DataMixin, ListView):
    model = Games
    template_name = 'games/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Games.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'games/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'games/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class GamesAPIView(generics.ListAPIView):
    queryset = Games.objects.all()
    serializer_class = GameSerializer
