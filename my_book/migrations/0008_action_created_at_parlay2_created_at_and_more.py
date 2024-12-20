# Generated by Django 5.1.3 on 2024-12-08 07:14

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_book", "0007_rename_single_bet_straight_single_bet1"),
    ]

    operations = [
        migrations.AddField(
            model_name="action",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="parlay2",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="parlay3",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="parlay4",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="singlebet",
            name="is_over",
            field=models.BooleanField(
                blank=True,
                help_text="True for 'Over' bets, False for 'Under' bets.",
                null=True,
            ),
        ),
    ]
