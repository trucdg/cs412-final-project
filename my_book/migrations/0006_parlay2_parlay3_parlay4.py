# Generated by Django 5.1.3 on 2024-11-28 22:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_book", "0005_action_straight_delete_bet"),
    ]

    operations = [
        migrations.CreateModel(
            name="Parlay2",
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
                        related_name="parlay2_bets",
                        to="my_book.player",
                    ),
                ),
                (
                    "single_bet1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parlay2_single_bet1",
                        to="my_book.singlebet",
                    ),
                ),
                (
                    "single_bet2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parlay2_single_bet2",
                        to="my_book.singlebet",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Parlay3",
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
                        related_name="parlay3_bets",
                        to="my_book.player",
                    ),
                ),
                (
                    "single_bet1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parlay3_single_bet1",
                        to="my_book.singlebet",
                    ),
                ),
                (
                    "single_bet2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parlay3_single_bet2",
                        to="my_book.singlebet",
                    ),
                ),
                (
                    "single_bet3",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parlay3_single_bet3",
                        to="my_book.singlebet",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Parlay4",
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
                        related_name="parlay4_bets",
                        to="my_book.player",
                    ),
                ),
                (
                    "single_bet1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parlay4_single_bet1",
                        to="my_book.singlebet",
                    ),
                ),
                (
                    "single_bet2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parlay4_single_bet2",
                        to="my_book.singlebet",
                    ),
                ),
                (
                    "single_bet3",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parlay4_single_bet3",
                        to="my_book.singlebet",
                    ),
                ),
                (
                    "single_bet4",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parlay4_single_bet4",
                        to="my_book.singlebet",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
