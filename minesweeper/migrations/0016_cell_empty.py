# Generated by Django 3.1.4 on 2021-02-20 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minesweeper', '0015_auto_20210218_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='empty',
            field=models.BooleanField(default=False),
        ),
    ]
