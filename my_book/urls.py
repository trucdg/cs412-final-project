from django.urls import path
from .views import (
    HomeView,
    PlayerListView,
    PlayerDetailView,
    PlayerUpdateView,
    PlayerDeleteView,
    GameListView,
    GameDetailView,
    GameUpdateView,
    GameDeleteView,
    BetListView,
    BetDetailView,
    BetCreateView,
    BetUpdateView,
    BetDeleteView,
    CalculatePayoutView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # Player URLs
    path(
        "players/", PlayerListView.as_view(), name="player-list"
    ),  # also handle player creation
    path("players/<int:pk>/", PlayerDetailView.as_view(), name="player-detail"),
    path("players/<int:pk>/edit/", PlayerUpdateView.as_view(), name="player-edit"),
    path("players/<int:pk>/delete/", PlayerDeleteView.as_view(), name="player-delete"),
    # Game URLs
    path(
        "games/", GameListView.as_view(), name="game-list"
    ),  # also handle game creation
    path("games/<int:pk>/", GameDetailView.as_view(), name="game-detail"),
    path("games/<int:pk>/edit/", GameUpdateView.as_view(), name="game-edit"),
    path("games/<int:pk>/delete/", GameDeleteView.as_view(), name="game-delete"),
    # Bet URLs
    path("bets/", BetListView.as_view(), name="bet-list"),
    path("bets/<int:pk>/", BetDetailView.as_view(), name="bet-detail"),
    path("bets/add/", BetCreateView.as_view(), name="bet-create"),
    path("bets/<int:pk>/edit/", BetUpdateView.as_view(), name="bet-update"),
    path("bets/<int:pk>/delete/", BetDeleteView.as_view(), name="bet-delete"),
    # Calculate Payout
    path("calculate-payout/", CalculatePayoutView.as_view(), name="calculate-payout"),
]
