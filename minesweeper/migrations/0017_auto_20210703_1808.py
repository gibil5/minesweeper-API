# Generated by Django 3.2.4 on 2021-07-03 23:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('minesweeper', '0016_cell_empty'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='board',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
