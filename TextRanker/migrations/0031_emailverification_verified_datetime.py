# Generated by Django 4.2.4 on 2024-07-17 18:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0030_alter_ticketlisting_original_purchase_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverification',
            name='verified_datetime',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 17, 13, 20, 5, 131555)),
            preserve_default=False,
        ),
    ]
