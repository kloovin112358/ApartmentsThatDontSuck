# Generated by Django 4.2.4 on 2024-09-05 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0076_alter_neighborhood_options_unit_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='live_search',
            field=models.BooleanField(default=True),
        ),
    ]
