# Generated by Django 3.1.4 on 2021-01-25 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minesweeper', '0005_board_mines'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='game_over',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='board',
            name='success',
            field=models.BooleanField(default=False),
        ),
    ]