from django import forms
from .models import SingleBet, Straight, Action, Parlay3, Parlay4, Player, Game


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ["name"]
        labels = {
            "name": "Player Name",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            "team_a",
            "team_b",
            "game_date",
            "fav",
            "fav_spread",
            "score_team_a",
            "score_team_b",
            "over_under_points",
        ]

        labels = {
            "team_a": "Team A",
            "team_b": "Team B",
            "game_date": "Game Date",
            "fav": "Favorite Team",
            "fav_spread": "Spread",
            "score_team_a": "Score (Team A)",
            "score_team_b": "Score (Team B)",
            "over_under_points": "Over/Under Points",
        }

        widgets = {
            "game_date": forms.DateInput(attrs={"type": "date"}),
        }


class BetTypeForm(forms.Form):
    BET_TYPE_CHOICES = [
        ("", "Pick a bet type"),  # Default placeholder value
        ("Straight", "Straight"),
        ("Action", "Action"),
        ("Parlay3", "Parlay 3"),
        ("Parlay4", "Parlay 4"),
    ]
    player = forms.ModelChoiceField(queryset=Player.objects.all())
    bet_type = forms.ChoiceField(choices=BET_TYPE_CHOICES)


class SingleBetForm(forms.ModelForm):
    class Meta:
        model = SingleBet
        fields = ["game", "single_bet_type", "selected_team", "is_over"]


class StraightBetForm(forms.ModelForm):
    class Meta:
        model = Straight
        fields = ["bet_amount"]


class ActionBetForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ["bet_amount"]


class Parlay3BetForm(forms.ModelForm):
    class Meta:
        model = Parlay3
        fields = ["bet_amount"]


class Parlay4BetForm(forms.ModelForm):
    class Meta:
        model = Parlay4
        fields = ["bet_amount"]


# Searching and Filtering Data
class BetTypeFilterForm(forms.Form):
    BET_TYPE_CHOICES = [
        ("", "All"),  # Option for displaying all bets
        ("Straight", "Straight"),
        ("Action", "Action"),
        ("Parlay3", "Parlay3"),
        ("Parlay4", "Parlay4"),
    ]

    bet_type_filter = forms.ChoiceField(
        choices=BET_TYPE_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={"class": "form-control", "id": "bet-type-filter-form"}
        ),
    )
