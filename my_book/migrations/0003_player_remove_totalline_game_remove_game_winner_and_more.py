# Generated by Django 5.1.3 on 2024-11-28 21:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_book", "0002_alter_spreadline_odds_team_b"),
    ]

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "total_betting_money",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
                ),
                (
                    "total_payout",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
                ),
            ],
        ),
        migrations.RemoveField(model_name="totalline", name="game",),
        migrations.RemoveField(model_name="game", name="winner",),
        migrations.AddField(
            model_name="game",
            name="fav",
            field=models.CharField(
                default=1, help_text="Favorite team of the game.", max_length=100
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="game",
            name="fav_spread",
            field=models.DecimalField(
                decimal_places=1,
                default=2,
                help_text="Spread for the favorite team (i.e: 3.0, 2.5)",
                max_digits=4,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="game",
            name="over_under_points",
            field=models.DecimalField(
                blank=True,
                decimal_places=1,
                help_text="Over/ Under points for both teams",
                max_digits=5,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="game",
            name="total_points",
            field=models.DecimalField(
                blank=True,
                decimal_places=1,
                help_text="Total points for both teams",
                max_digits=5,
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="SingleBet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "single_bet_type",
                    models.CharField(
                        choices=[("WINNER", "Winner"), ("OVER-UNDER", "Over-Under")],
                        max_length=20,
                    ),
                ),
                (
                    "selected_team",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("is_over", models.BooleanField(blank=True, null=True)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="straights",
                        to="my_book.game",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Bet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "bet_type",
                    models.CharField(
                        choices=[
                            ("STRAIGHT", "Straight"),
                            ("ACTION", "Action"),
                            ("PARLAY2", "Parlay2"),
                            ("PARLAY3", "Parlay3"),
                            ("PARLAY4", "Parlay4"),
                        ],
                        max_length=10,
                    ),
                ),
                ("bet_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "payout",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "outcome",
                    models.CharField(
                        blank=True,
                        choices=[("WIN", "Win"), ("LOSE", "Lose"), ("PUSH", "Push")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bets",
                        to="my_book.player",
                    ),
                ),
                (
                    "bet_list",
                    models.ManyToManyField(related_name="bets", to="my_book.singlebet"),
                ),
            ],
        ),
        migrations.DeleteModel(name="SpreadLine",),
        migrations.DeleteModel(name="TotalLine",),
    ]
