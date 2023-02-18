import json

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models import OuterRef, Subquery, Max, Min
from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import game, settings


def home(request):
    return render(request, 'storage/home.html')

class GameListView(LoginRequiredMixin, ListView):
    model = game
    template_name = 'storage/game_list.html'
    context_object_name = 'games'
    ordering = ['-attempted']
    paginate_by = 25

    # TODO: add duration here
    def get_queryset(self):
        user = self.request.user
        # iterate over all games and add duration
        queryset = user.games.all().order_by('-attempted')
        for game in queryset:
            game.duration = json.loads(game.params)['duration']
        return queryset


class LeaderboardView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'storage/leaderboard.html'
    # ordering = ['-score', 'attempted']
    context_object_name = 'users'
    paginate_by = 25

    def get_queryset(self):

        # Subquery to get the max score of games for a user
        max_score_subquery = game.objects.filter(user=OuterRef('pk')).values('user').annotate(max_score=Max('score')).values('max_score')

        # Subquery to get the earliest game for a user with the max score
        earliest_max_score_game_subquery = game.objects.filter(user=OuterRef('pk'), score=OuterRef('max_score')).values('attempted').order_by('attempted')[:1]

        users = User.objects.annotate(
            max_score=Subquery(max_score_subquery),
            attempted=Subquery(earliest_max_score_game_subquery)
        )

        return users.order_by('-max_score', 'attempted')


class settingsForm(forms.ModelForm):
    duration = forms.ChoiceField(
        choices=[(30, '30'), (60, '60'), (120, '120'), (300, '300'), (600, '600')])

    class Meta:
        model = settings
        fields = ['add', 'sub', 'mul', 'div', 'duration', 'add_left_min', 'add_left_max', 'add_right_min',
                  'add_right_max', 'mul_left_min', 'mul_left_max', 'mul_right_min', 'mul_right_max']


class SettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = settings
    template_name = 'storage/settings.html'
    form_class = settingsForm

    def get_object(self):
        return self.request.user.settings

    def get_success_url(self):
        return '/settings'
