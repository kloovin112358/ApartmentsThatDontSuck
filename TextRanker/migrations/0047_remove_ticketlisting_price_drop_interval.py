# Generated by Django 4.2.4 on 2024-07-23 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0046_remove_ticketlisting_smart_pricing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketlisting',
            name='price_drop_interval',
        ),
    ]
