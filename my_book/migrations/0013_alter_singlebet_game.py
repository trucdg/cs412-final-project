# Generated by Django 5.1.4 on 2024-12-09 01:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_book", "0012_delete_parlay2"),
    ]

    operations = [
        migrations.AlterField(
            model_name="singlebet",
            name="game",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="single_bets",
                to="my_book.game",
            ),
        ),
    ]