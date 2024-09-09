# Generated by Django 4.2.4 on 2024-07-19 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0040_customuser_ban_removal_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketpurchase',
            name='payment_transfer_datetime',
            field=models.DateTimeField(blank=True, help_text='Time that payment was cleared.', null=True),
        ),
    ]