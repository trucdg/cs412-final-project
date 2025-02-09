# Generated by Django 5.1.3 on 2024-11-28 21:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "my_book",
            "0004_alter_game_over_under_points_alter_game_score_team_a_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Action",
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
                ("bet_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "payout",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="action_bets",
                        to="my_book.player",
                    ),
                ),
                (
                    "single_bet1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="action_single_bet1",
                        to="my_book.singlebet",
                    ),
                ),
                (
                    "single_bet2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="action_single_bet2",
                        to="my_book.singlebet",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Straight",
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
                ("bet_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "payout",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="straight_bets",
                        to="my_book.player",
                    ),
                ),
                (
                    "single_bet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="straight_bets",
                        to="my_book.singlebet",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.DeleteModel(name="Bet",),
    ]
