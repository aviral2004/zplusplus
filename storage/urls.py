from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.GameListView.as_view(), name='games'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('settings/', views.SettingsUpdateView.as_view(), name='settings'),
]
