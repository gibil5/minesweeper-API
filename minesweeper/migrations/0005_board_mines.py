# Generated by Django 3.1.4 on 2021-01-25 00:20

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minesweeper', '0004_auto_20210124_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='mines',
            #field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None), default=0, size=None),
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None), default=[], size=None),
            preserve_default=False,
        ),
    ]