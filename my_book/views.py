from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.views import View
from .models import Player, Game, Bet, SingleBet
from .models import Straight, Action, Parlay3, Parlay4
from .forms import BetTypeForm, SingleBetForm, GameForm, PlayerForm
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
import json
from itertools import chain
from operator import attrgetter


class HomeView(TemplateView):
    """
    Class-based view for the homepage.
    """

    template_name = "my_book/home.html"


# Player Views
class PlayerListView(ListView):
    """
    A View to list out Player and a summary of their betting money and payout
    - handles create new player post requests
    """

    model = Player
    template_name = "players/player_list.html"
    context_object_name = "players"

    def get_context_data(self, **kwargs):
        # Add the form to the context
        context = super().get_context_data(**kwargs)
        if "player_form" not in context:
            context["player_form"] = PlayerForm()

        # Fetch all players with their calculated fields
        players = Player.objects.all()

        # update all calculated money
        for player in players:
            player.calculate_total_betting_money()
            player.calculate_total_payout()

        context["players"] = players

        return context

    def post(self, request, *args, **kwargs):
        """Handle player creation when the form is submitted."""
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()  # Create a new player instance
            return redirect("player-list")
        else:
            context = self.get_context_data()
            context["player_form"] = (
                form  # Pass the form with errors back to the template
            )
            return self.render_to_response(context)


class PlayerUpdateView(UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = "players/player_edit.html"
    context_object_name = "player"

    def get_success_url(self):
        # Redirect to the player list after editing
        return reverse_lazy("player-list")


class PlayerDetailView(DetailView):
    model = Player
    template_name = "players/player_detail.html"
    context_object_name = "player"


class PlayerDeleteView(DeleteView):
    model = Player
    template_name = "players/player_delete.html"
    success_url = reverse_lazy("player-list")
    context_object_name = "player"


class GameListView(View):
    """
    A view class to display a list of all games,
    and handle create new game form submission
    """

    def get(self, request, *args, **kwargs):
        games = Game.objects.all().order_by("-game_date")
        form = GameForm()
        return render(request, "games/game_list.html", {"games": games, "form": form})

    def post(self, request, *args, **kwargs):
        """
        Add new game form is on the top of the GameListView
        Thus, I use this to handle  create new game form submission
        post to the game-list url
        """
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new game to the database
            return redirect("game-list")  # Replace with the name of your games list URL
        games = Game.objects.all().order_by("-game_date")
        return render(request, "games/game_list.html", {"games": games, "form": form})


class GameDetailView(DetailView):
    """
    Class-based view for displaying detailed information about a specific game.
    """

    model = Game
    template_name = "games/game_detail.html"
    context_object_name = "game"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()

        return context


class GameUpdateView(UpdateView):
    """
    A view class to update Game detail
    """

    model = Game
    form_class = GameForm
    template_name = "games/game_edit.html"
    success_url = reverse_lazy("game-list")


class GameDeleteView(DeleteView):
    model = Game
    template_name = "games/game_delete.html"
    success_url = reverse_lazy("game-list")
    context_object_name = "game"


# Bet Views
class BetListView(ListView):
    template_name = "bets/bet_list.html"
    SingleBetFormSet = formset_factory(SingleBetForm, extra=0)

    def get_queryset(self):
        # Fetch all bets from different models
        straight_bets = Straight.objects.all()
        action_bets = Action.objects.all()
        parlay3_bets = Parlay3.objects.all()
        parlay4_bets = Parlay4.objects.all()

        # Combine all the querysets into one list
        all_bets = list(chain(straight_bets, action_bets, parlay3_bets, parlay4_bets))

        # Order the combined list by the 'created_at' field
        all_bets.sort(key=attrgetter("created_at"), reverse=True)

        return all_bets

    def get_context_data(self, bet_type_form=None, single_bet_forms=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # if default forms are not provided, create new
        if bet_type_form is None:
            bet_type_form = BetTypeForm()
        if single_bet_forms is None:
            single_bet_forms = self.SingleBetFormSet()

        # Fetch all available games
        games = Game.objects.all().values(
            "id", "team_a", "team_b", "game_date", "fav_spread", "over_under_points"
        )

        # Flatten the bet objects into a list with global index
        bets_flat = self._get_flat_bet_list()

        context["bet_type_form"] = bet_type_form
        context["single_bet_forms"] = single_bet_forms
        context["bets_flat"] = bets_flat
        context["games_json"] = mark_safe(
            json.dumps(list(games), cls=DjangoJSONEncoder)
        )

        return context

    def post(self, request, *args, **kwargs):
        """
        Handle bet creation and deletion form submission.
        """
        # Ensure `object_list` is populated
        self.object_list = self.get_queryset()

        # handle bet DELETION
        if "delete_bet_pk" in request.POST:
            print("IN DELETE BET")
            return self.delete_bet(request)

        bet_type_form = BetTypeForm(request.POST)
        single_bet_forms = self.SingleBetFormSet(request.POST)

        print(f"request.POST: {request.POST}")

        # print(f"in POST: bet_type_form.is_valid={bet_type_form.is_valid()}")
        # print(f"in POST: single_bet_forms.is_valid={single_bet_forms.is_valid()}")
        # print(f"in POST: {single_bet_forms.errors}")

        if not single_bet_forms.is_valid():
            for form in single_bet_forms:
                if not form.is_valid():
                    print(f"Form errors: {form.errors}")
            print(f"Non-form errors: {single_bet_forms.non_form_errors()}")

        # Initial Validation Check: This block ensures that the top-level forms
        # (BetTypeForm and the SingleBetFormSet) are valid.
        # if the Forms are not valid, rerender the page
        if not bet_type_form.is_valid() or not single_bet_forms.is_valid():
            return self._re_render_with_context(
                request, bet_type_form, single_bet_forms
            )

        # Extract the necessary data from request.POST
        post_data = request.POST

        # Extract bet type and create the appropriate form
        player_id = post_data["player"]
        bet_type = post_data["bet_type"]
        bet_amount = post_data["bet_amount"]

        # get the player instance
        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            print("User with the specified name does not exist.")

        single_bets = []

        # Iterate through the total forms to create SingleBet instances
        for i in range(len(single_bet_forms)):
            try:
                # Dynamically construct field names
                game_id = post_data.get(f"single_bet_{i}_game")
                single_bet_type = post_data.get(f"single_bet_{i}_single_bet_type")
                selected_team = post_data.get(f"single_bet_{i}_selected_team")
                is_over = (
                    post_data.get(f"single_bet_{i}_is_over") == "on"
                )  # Convert checkbox to boolean

                # Ensure the Game instance exists
                game = Game.objects.get(id=game_id)

                # Create the SingleBet instance
                single_bet = SingleBet(
                    game=game,
                    single_bet_type=single_bet_type,
                    selected_team=selected_team,
                    is_over=(
                        is_over if single_bet_type == "OVER-UNDER" else None
                    ),  # Apply only if relevant
                )

                # save the single bet instance so that we can use to create the other bet type
                single_bet.save()

                single_bets.append(single_bet)

                print(f"BetListView.post(): created SingleBet= {single_bet}")

            except Game.DoesNotExist:
                print(
                    f"Game with ID {game_id} does not exist. Skipping this SingleBet."
                )
            except Exception as e:
                print(f"Error creating SingleBet for form {i}: {e}")

        # Now that we have enough information, we can create the bet object
        bet = self.create_bet(bet_type, player, bet_amount, single_bets)

        # Redirect to refresh the page
        return redirect(reverse("bet-list"))

    def delete_bet(self, request):
        """
        Handle bet deletion
        This checks the bet type and deletes from the correct model.
        """

        print("IN DELETE BET")
        if request.method != "POST":
            print("BetListView.delete_bet(): NOT a POST request!")
            return redirect("bet-list")

        bet_id = request.POST.get("delete_bet_pk")
        if not bet_id:
            print("BetListView.delete_bet(): bet_id is required")
            return redirect("bet-list")

        bet_type = request.POST.get("delete_bet_type")
        if not bet_type:
            print("BetListView.delete_bet(): bet_type is required ")
            return redirect("bet-list")

        try:
            # Determine the model based on bet type and get the bet instance
            if bet_type == "Straight":
                bet = get_object_or_404(Straight, id=bet_id)
            elif bet_type == "Action":
                bet = get_object_or_404(Action, id=bet_id)
            elif bet_type == "Parlay3":
                bet = get_object_or_404(Parlay3, id=bet_id)
            elif bet_type == "Parlay4":
                bet = get_object_or_404(Parlay4, id=bet_id)
            else:
                print("BetListView.delete_bet(): Invalid bet type")
                return redirect("bet-list")

            # Delete the bet instance
            bet.delete()
            print(f"{bet_type}(pk={bet_id}) bet deleted successfully.")

        except Exception as e:
            print(f"BetListView.delete_bet(): Error {str(e)}")

        # Redirect to the bet list view
        return redirect("bet-list")

    def create_bet(self, bet_type, player, bet_amount, single_bets):
        """
        Create a bet instance based on the bet_type and a list of SingleBet instances.

        input:
            bet_type (str): The type of bet (e.g., "Straight", "Action", "Parlay3", "Parlay4").
            player (Player): The player placing the bet.
            bet_amount (Decimal): The amount of the bet.
            single_bets (list): A list of SingleBet instances.

        Returns:
            Bet instance: The created bet instance.
        """
        try:
            if bet_type == "Straight" and len(single_bets) == 1:
                bet = Straight(
                    player=player,
                    bet_amount=bet_amount,
                    single_bet1=single_bets[0],
                )

            elif bet_type == "Action" and len(single_bets) == 2:
                bet = Action(
                    player=player,
                    bet_amount=bet_amount,
                    single_bet1=single_bets[0],
                    single_bet2=single_bets[1],
                )

            elif bet_type == "Parlay3" and len(single_bets) == 3:
                bet = Parlay3(
                    player=player,
                    bet_amount=bet_amount,
                    single_bet1=single_bets[0],
                    single_bet2=single_bets[1],
                    single_bet3=single_bets[2],
                )

            elif bet_type == "Parlay4" and len(single_bets) == 4:
                bet = Parlay4(
                    player=player,
                    bet_amount=bet_amount,
                    single_bet1=single_bets[0],
                    single_bet2=single_bets[1],
                    single_bet3=single_bets[2],
                    single_bet4=single_bets[3],
                )

            else:
                raise ValueError(
                    f"Invalid bet type or mismatched SingleBet count for {bet_type}."
                )

            # Validate and save the bet instance
            bet.full_clean()  # Run model validation
            bet.save()
            print(f"BetListView.create_bet(): Created {bet_type} bet: {bet}")
            return bet

        except Exception as e:
            print(f"BetListView.create_bet(): Error creating {bet_type} bet: {e}")
            return None

    def _re_render_with_context(self, request, bet_type_form, single_bet_forms):
        """
        re-render the page with updated context
        """
        context = self.get_context_data(
            bet_type_form=bet_type_form, single_bet_forms=single_bet_forms
        )
        return render(self.request, self.template_name, context)

    def _get_flat_bet_list(self):
        """
        Flatten the bet list for context.
        """
        bets = {
            "Straight": Straight.objects.all(),
            "Action": Action.objects.all(),
            "Parlay3": Parlay3.objects.all(),
            "Parlay4": Parlay4.objects.all(),
        }

        bets_flat = []
        index = 1
        for bet_type, bet_list in bets.items():
            for bet in bet_list:
                # Extract single bets dynamically
                single_bets = []
                for i in range(1, 5):  # Up to 4 single bets
                    single_bet_attr = f"single_bet{i}"
                    if hasattr(bet, single_bet_attr):
                        single_bet = getattr(bet, single_bet_attr, None)
                        single_bets.append(single_bet)
                    else:
                        single_bets.append(None)  # Append None for missing single bets

                # Add bet details
                bets_flat.append(
                    {
                        "index": index,
                        "bet_pk": bet.pk,
                        "player_name": bet.player.name,
                        "bet_type": bet_type,
                        "amount": bet.bet_amount,
                        "payout": bet.payout,
                        "single_bet1": single_bets[0] if len(single_bets) > 0 else None,
                        "single_bet2": single_bets[1] if len(single_bets) > 1 else None,
                        "single_bet3": single_bets[2] if len(single_bets) > 2 else None,
                        "single_bet4": single_bets[3] if len(single_bets) > 3 else None,
                    }
                )
                index += 1
        return bets_flat

    def get_bet_details(self, bet, bet_type):
        if bet_type == "Straight":
            return bet.single_bet
        elif bet_type == "Action":
            return f"{bet.single_bet1} and {bet.single_bet2}"
        elif bet_type == "Parlay3":
            return f"{bet.single_bet1}, {bet.single_bet2}, {bet.single_bet3}"
        elif bet_type == "Parlay4":
            return f"{bet.single_bet1}, {bet.single_bet2}, {bet.single_bet3}, {bet.single_bet4}"
        return ""


class BetDetailView(DetailView):
    model = Bet
    template_name = "bets/bet_detail.html"
    context_object_name = "bet"


class BetUpdateView(UpdateView):
    model = Bet
    template_name = "bets/bet_form.html"
    fields = ["player", "bet_type", "bet_list", "bet_amount", "payout", "outcome"]
    success_url = reverse_lazy("bet-list")


class BetDeleteView(DeleteView):
    model = Bet
    template_name = "bets/bet_confirm_delete.html"
    success_url = reverse_lazy("bet-list")


class BetCreateView(CreateView):
    model = Bet
    template_name = "bets/bet_form.html"
    fields = ["player", "bet_type", "bet_list", "bet_amount", "payout", "outcome"]
    success_url = reverse_lazy("bet-list")


class CalculatePayoutView(View):
    """
    A view class to calculate the payout for all bets if scores available
    """

    def post(self, request, *args, **kwargs):
        """
        when received a post request to calculate all payout
        """
        # Collect all bet types
        all_bets = [
            Straight.objects.all(),
            Action.objects.all(),
            Parlay3.objects.all(),
            Parlay4.objects.all(),
        ]

        # Iterate through each bet and calculate payout
        for bet_queryset in all_bets:
            for bet in bet_queryset:  # Iterate through each individual bet
                bet.calculate_payout()  # Call calculate_payout on each bet
                # print(f"CALCULATE bet {bet}")
                # print(f"CALCULATE bet_payout {bet.payout}")

        # Redirect back to the bet list page
        return redirect("bet-list")
