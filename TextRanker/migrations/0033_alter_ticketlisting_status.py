# Generated by Django 4.2.4 on 2024-07-17 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0032_alter_ticketlisting_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketlisting',
            name='status',
            field=models.CharField(choices=[('Live', 'Live'), ('Cancelled', 'Cancelled - Listing taken down by seller'), ('Listed - Verif. Hold', 'Listed - hold for ticket verification by seller'), ('Listed - Verif. Expired', 'Listed - Seller failed to verify ticket in time'), ('In Cart - Checkout Hold', 'In Cart - Hold for prospective buyer in checkout process'), ('On Hold - Reported Hold', 'On Hold - Hold due to listing reported'), ('Force Removed', 'Removed by staff due to violation of policy'), ('Sold - Awaiting Transfer', 'Sold - Awaiting ticket transfer'), ('Sold - Awaiting Payment Transfer to Seller', 'Sold - Awaiting Payment Transfer to Seller'), ('Sold', 'Ticket sold successfully'), ('Unsold', 'Ticket not sold before event start time')], max_length=50),
        ),
    ]