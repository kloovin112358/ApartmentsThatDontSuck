# Generated by Django 4.2.4 on 2024-07-12 15:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0008_eventregion_region_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketlisting',
            name='price_drop_interval',
            field=models.PositiveSmallIntegerField(blank=True, help_text='After how many days would you like to drop the price by the specified interval?', null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
