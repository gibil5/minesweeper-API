# Generated by Django 3.1.4 on 2021-01-25 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minesweeper', '0003_board_flags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='mines',
            new_name='nr_mines',
        ),
    ]
