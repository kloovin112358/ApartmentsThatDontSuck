# Generated by Django 4.2.4 on 2024-07-18 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0038_ticket_ticket_live_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketpurchase',
            name='payment_transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]