# Generated by Django 3.1.4 on 2021-01-26 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minesweeper', '0008_board_nr_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='board',
            name='state',
            field=models.CharField(blank=True, choices=[('BEGIN', 'Begin'), ('IN_PROGRESS', 'In progress'), ('PAUSE', 'Pause'), ('END', 'End')], max_length=16, null=True),
        ),
    ]
