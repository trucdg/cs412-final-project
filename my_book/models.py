from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Sum


# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)
    total_betting_money = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00
    )
    total_payout = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

    def get_straight_bet_count(self):
        """Return the number of Straight bets this player has made."""
        return self.straight_bets.count()

    def get_action_bet_count(self):
        """Return the number of Action bets this player has made."""
        return self.action_bets.count()

    def get_parlay3_bet_count(self):
        """Return the number of Parlay 3 bets this player has made."""
        return self.parlay3_bets.count()

    def get_parlay4_bet_count(self):
        """Return the number of Parlay 4 bets this player has made."""
        return self.parlay4_bets.count()

    def calculate_total_betting_money(self):
        """Using aggregate to sum up bet amounts for all bet types"""
        total_betting_money = self.straight_bets.aggregate(total=Sum("bet_amount"))[
            "total"
        ] or Decimal(0)
        total_betting_money += self.action_bets.aggregate(total=Sum("bet_amount"))[
            "total"
        ] or Decimal(0)
        total_betting_money += self.parlay3_bets.aggregate(total=Sum("bet_amount"))[
            "total"
        ] or Decimal(0)
        total_betting_money += self.parlay4_bets.aggregate(total=Sum("bet_amount"))[
            "total"
        ] or Decimal(0)
        return total_betting_money

    def calculate_total_payout(self):
        # Sum payouts for all bet types
        total_payout = 0
        # Sum payout for all bet types
        for bet_model in [
            self.straight_bets,
            self.action_bets,
            self.parlay3_bets,
            self.parlay4_bets,
        ]:
            for bet in bet_model.all():
                total_payout += bet.calculate_payout()
        return total_payout


class Game(models.Model):
    team_a = models.CharField(max_length=100)  # Name of Team A
    team_b = models.CharField(max_length=100)  # Name of Team B
    game_date = models.DateField()
    fav = models.CharField(
        max_length=100,
        help_text="Favorite team of the game.",
    )

    fav_spread = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        help_text="Spread for the favorite team (i.e: 3.0, 2.5)",
    )

    score_team_a = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        default=0.0,
        help_text="Final score for Team A.",
    )
    score_team_b = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        default=0.0,
        help_text="Final score for Team B.",
    )

    total_points = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        default=0.0,
        help_text="Total points for both teams",
    )

    over_under_points = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        help_text="Over/ Under points for both teams",
    )

    def determine_winner(self):
        """
        Determine the winner using the score
        The favorite team wins if (its score + fav_spread) > the underdog score
        Output:
        - team name of the winner
        - 'Tie' otherwise
        - None if no result is available
        """
        if self.score_team_a is None or self.score_team_b is None:
            return None  # Scores not available

        # Adjust scores based on the favorite and underdog
        if self.fav == self.team_a:
            adjusted_team_a_score = self.score_team_a - self.fav_spread
            adjusted_team_b_score = self.score_team_b
        elif self.fav == self.team_b:
            adjusted_team_a_score = self.score_team_a
            adjusted_team_b_score = self.score_team_b - self.fav_spread
        else:
            return None  # Invalid favorite team

        # Determine winner
        if adjusted_team_a_score > adjusted_team_b_score:
            return self.team_a
        elif adjusted_team_a_score < adjusted_team_b_score:
            return self.team_b
        else:
            return "Tie"

    def determine_over_under(self):
        """
        Determine the outcome of the over/ under bet
        Output:
        - 'Over', 'Under' or 'Tie' if total points for both team == over_under_points
        - None if total_points are not available
        """
        if self.total_points is None or self.over_under_points is None:
            print(
                "Game.determne_winner(): total_points or over_under_points are not available."
            )
            return None
        if self.total_points > self.over_under_points:
            return "Over"
        elif self.total_points < self.over_under_points:
            return "Under"
        else:
            # self.total_points == self.over_under_points:
            return "Tie"

    def save(self, *args, **kwargs):
        # Automatically calculate total points if scores are provided
        if self.score_team_a is not None and self.score_team_b is not None:
            self.total_points = self.score_team_a + self.score_team_b

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team_a}@{self.team_b}"


class SingleBet(models.Model):
    SINGLE_BET_TYPES = [
        ("WINNER", "Winner"),
        ("OVER-UNDER", "Over-Under"),
    ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="single_bets")
    single_bet_type = models.CharField(max_length=20, choices=SINGLE_BET_TYPES)
    selected_team = models.CharField(
        max_length=100, blank=True, null=True
    )  # For "Winner" bets
    is_over = models.BooleanField(
        blank=True,
        null=True,
        help_text="True for 'Over' bets, False for 'Under' bets.",
    )  # True if betting "Over", False for "Under"

    def determine_outcome(self):
        """
        Determine if bet is Win, Loss or Tie
        Returns:
        - 'Win', 'Loss', or 'Tie'
        - 'Invalid' if the bet or game state is invalid
        """
        if not self.game:
            return "Invalid"

        if self.single_bet_type == "WINNER":
            winner = self.game.determine_winner()
            if winner == "Tie":
                return "Tie"
            elif winner == self.selected_team:
                return "Win"
            else:
                return "Loss"
        elif self.single_bet_type == "OVER-UNDER":
            over_under_outcome = self.game.determine_over_under()
            if over_under_outcome == "Tie":
                return "Tie"
            elif over_under_outcome == "Over" and self.is_over:
                return "Win"
            elif over_under_outcome == "Under" and not self.is_over:
                return "Win"
            else:
                return "Loss"
        else:
            return "Invalid"

    def __str__(self):
        # Handle "WINNER" bet type
        if self.single_bet_type == "WINNER" and self.selected_team:
            return f"{self.game}: WINNER {self.selected_team}"

        # Handle "OVER-UNDER" bet type
        elif self.single_bet_type == "OVER-UNDER":
            if self.is_over is not None:
                return f"{self.game}: {'OVER' if self.is_over else 'UNDER'} {self.game.over_under_points}"
            else:
                return f"{self.game}: Missing O/U points"

        # Fallback in case bet type is neither "WINNER" nor "OVER-UNDER"
        return f"{self.game}: Unknown Bet Type"


class Bet(models.Model):
    """
    Abstract class for different bet types
    """

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="bets")
    bet_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payout = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Bet: {self.player} (amount: {self.bet_amount})"


class Straight(Bet):
    """
    A bet type that contains only 1 single bet
    """

    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="straight_bets"
    )
    single_bet1 = models.ForeignKey(
        SingleBet, on_delete=models.CASCADE, related_name="straight_bets"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.single_bet1:
            raise ValidationError(
                "A straight bet must be associated with exactly 1 SingleBet."
            )

    def calculate_payout(self):
        """
        For Straight, the payout multiplier is:
        - Win: 1
        - Tie: 0
        - Loss: -1
        If Loss, need to pay 5% commission
        """
        # Get the outcome from the single bet
        outcome = self.single_bet1.determine_outcome()

        # Determine the payout multiplier based on the outcome
        if outcome == "Win":
            multiplier = Decimal(1)
        elif outcome == "Tie":
            multiplier = Decimal(0)
        elif outcome == "Loss":
            multiplier = Decimal(-1.05)  # includes 5% comission
        else:
            raise ValueError("Invalid outcome for the bet.")

        # Calculate the payout
        payout = self.bet_amount * multiplier
        # Round the payout to 2 decimal places
        self.payout = payout.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        # Save the calculated payout in the database
        self.save()

        return self.payout

    def __str__(self):
        return f"Straight: {self.player} - {self.single_bet1}"


class Action(Bet):
    """
    A bet type that contains 2 single bets
    """

    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="action_bets"
    )
    single_bet1 = models.ForeignKey(
        SingleBet, on_delete=models.CASCADE, related_name="action_single_bet1"
    )
    single_bet2 = models.ForeignKey(
        SingleBet, on_delete=models.CASCADE, related_name="action_single_bet2"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_payout(self):
        """
        For Action, the payout multiplier is as follow
        Multiplier - Outcome set of single bets:
        1:4 -  {"Win", "Win"}
        1:2 -  {"Win", "Tie"}
        1:0 -  {"Tie", "Tie"}
        1:(-1.1) - if either single bets outcome are "Loss",
                   a (-1.1) multiplier is appliedto pay 10% commission.
        """

        # Determine outcomes of both single bets
        outcome1 = self.single_bet1.determine_outcome()
        outcome2 = self.single_bet2.determine_outcome()

        # Define the payout multiplier
        if outcome1 == "Loss" or outcome2 == "Loss":
            multiplier = Decimal(-1.1)  # 10% commission
        elif outcome1 == "Win" and outcome2 == "Win":
            multiplier = Decimal(4)
        elif ("Win" in {outcome1, outcome2}) and ("Tie" in {outcome1, outcome2}):
            multiplier = Decimal(2)
        elif outcome1 == "Tie" and outcome2 == "Tie":
            multiplier = Decimal(0)
        else:
            raise ValueError("Invalid outcomes for the bets.")

        # Calculate the payout
        payout = self.bet_amount * multiplier
        # Round the payout to 2 decimal places
        self.payout = payout.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Save the calculated payout in the database
        self.save()

        return self.payout

    def clean(self):
        # Check if both single_bets are provided
        if not self.single_bet1 or not self.single_bet2:
            raise ValidationError(
                "An action bet must be associated with exactly 2 SingleBets."
            )

        # Ensure that single_bet1 and single_bet2 are not the same
        if self.single_bet1 == self.single_bet2:
            raise ValidationError("single_bet1 and single_bet2 must be different.")

    def __str__(self):
        return f"Action: {self.player} - {self.single_bet1}, {self.single_bet2}"


class Parlay3(Bet):
    """
    A bet type that contains 3 single bets
    """

    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="parlay3_bets"
    )
    single_bet1 = models.ForeignKey(
        SingleBet, on_delete=models.CASCADE, related_name="parlay3_single_bet1"
    )
    single_bet2 = models.ForeignKey(
        SingleBet, on_delete=models.CASCADE, related_name="parlay3_single_bet2"
    )
    single_bet3 = models.ForeignKey(
        SingleBet, on_delete=models.CASCADE, related_name="parlay3_single_bet3"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_payout(self):
        """
        For Parlay 3:
        Multiplier - Outcome set of single bets:
            1:6 -  {"Win", "Win", "Win"}
            1:4 -  {"Win", "Win", "Tie"}
            1:1 -  {"Win", "Tie", "Tie"}
            1:0 -  {"Tie", "Tie", "Tie"}
            1:(-1) - if any single bets outcome is "Loss",
        """

        # Determine outcomes of all three single bets
        outcome1 = self.single_bet1.determine_outcome()
        outcome2 = self.single_bet2.determine_outcome()
        outcome3 = self.single_bet3.determine_outcome()

        # Define the payout multiplier
        if "Loss" in {outcome1, outcome2, outcome3}:
            multiplier = Decimal(
                -1
            )  # Loss in any bet results in loss of the parlay bet
        elif outcome1 == "Win" and outcome2 == "Win" and outcome3 == "Win":
            multiplier = Decimal(6)  # All three bets win
        elif outcome1 == "Win" and outcome2 == "Win" and outcome3 == "Tie":
            multiplier = Decimal(4)  # Two wins, one tie
        elif outcome1 == "Win" and outcome2 == "Tie" and outcome3 == "Tie":
            multiplier = Decimal(1)  # One win, two ties
        elif outcome1 == "Tie" and outcome2 == "Tie" and outcome3 == "Tie":
            multiplier = Decimal(0)  # All bets tie
        else:
            raise ValueError("Invalid outcome combination for the parlay bet.")

        # Calculate the payout
        payout = self.bet_amount * multiplier
        # Round the payout to 2 decimal places
        self.payout = payout.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Save the calculated payout in the database
        self.save()

        return self.payout

    def clean(self):
        # Create a set of the SingleBets
        single_bets = {self.single_bet1, self.single_bet2, self.single_bet3}

        # Ensure exactly 3 unique SingleBets are associated
        if len(single_bets) != 3:
            raise ValidationError("All SingleBets for a parlay3 bet must be unique.")

    def __str__(self):
        return f"Parlay3: {self.player} - {self.single_bet1}, {self.single_bet2}, {self.single_bet3}"


class Parlay4(Bet):
    """
    A bet type that contains 4 single bets
    """

    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="parlay4_bets"
    )
    single_bet1 = models.ForeignKey(
        SingleBet, on_delete=models.CASCADE, related_name="parlay4_single_bet1"
    )
    single_bet2 = models.ForeignKey(
        SingleBet, on_delete=models.CASCADE, related_name="parlay4_single_bet2"
    )
    single_bet3 = models.ForeignKey(
        SingleBet, on_delete=models.CASCADE, related_name="parlay4_single_bet3"
    )
    single_bet4 = models.ForeignKey(
        SingleBet, on_delete=models.CASCADE, related_name="parlay4_single_bet4"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_payout(self):
        """
        For Parlay 4:
        Multiplier - Outcome set of single bets:
            1:10 -  {"Win", "Win", "Win", "Win"}
            1:6  -  {"Win", "Win", "Win", "Tie"}
            1:4  -  {"Win", "Win", "Tie", "Tie"}
            1:1  -  {"Win", "Tie", "Tie", "Tie"}
            1:0  -  {"Tie", "Tie", "Tie", "Tie"}
            1:(-1) - if any single bets outcome is "Loss",
        """
        # Determine outcomes of all four single bets
        outcome1 = self.single_bet1.determine_outcome()
        outcome2 = self.single_bet2.determine_outcome()
        outcome3 = self.single_bet3.determine_outcome()
        outcome4 = self.single_bet4.determine_outcome()

        # Define the payout multiplier
        if "Loss" in {outcome1, outcome2, outcome3, outcome4}:
            multiplier = Decimal(
                -1
            )  # Loss in any bet results in loss of the parlay bet
        elif (
            outcome1 == "Win"
            and outcome2 == "Win"
            and outcome3 == "Win"
            and outcome4 == "Win"
        ):
            multiplier = Decimal(10)  # All four bets win
        elif (
            outcome1 == "Win"
            and outcome2 == "Win"
            and outcome3 == "Win"
            and outcome4 == "Tie"
        ):
            multiplier = Decimal(6)  # Three wins, one tie
        elif (
            outcome1 == "Win"
            and outcome2 == "Win"
            and outcome3 == "Tie"
            and outcome4 == "Tie"
        ):
            multiplier = Decimal(4)  # Two wins, two ties
        elif (
            outcome1 == "Win"
            and outcome2 == "Tie"
            and outcome3 == "Tie"
            and outcome4 == "Tie"
        ):
            multiplier = Decimal(1)  # One win, three ties
        elif (
            outcome1 == "Tie"
            and outcome2 == "Tie"
            and outcome3 == "Tie"
            and outcome4 == "Tie"
        ):
            multiplier = Decimal(0)  # All bets tie
        else:
            raise ValueError("Invalid outcome combination for the parlay bet.")

        # Calculate the payout
        payout = self.bet_amount * multiplier
        # Round the payout to 2 decimal places
        self.payout = payout.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.save()

        return self.payout

    def clean(self):
        # Create a set of the SingleBets
        single_bets = {
            self.single_bet1,
            self.single_bet2,
            self.single_bet3,
            self.single_bet4,
        }

        # Ensure exactly 4 unique SingleBets are associated
        if len(single_bets) != 4:
            raise ValidationError("All SingleBets for a parlay4 bet must be unique.")

    def __str__(self):
        return f"Parlay4: {self.player} - {self.single_bet1}, {self.single_bet2}, {self.single_bet3}, {self.single_bet4}"
