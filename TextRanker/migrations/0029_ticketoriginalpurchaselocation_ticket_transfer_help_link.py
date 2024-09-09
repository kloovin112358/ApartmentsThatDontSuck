# Generated by Django 4.2.4 on 2024-07-16 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0028_eventregion_google_maps_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketoriginalpurchaselocation',
            name='ticket_transfer_help_link',
            field=models.URLField(blank=True, help_text='Link to the site help page for ticket transfers.', null=True),
        ),
    ]