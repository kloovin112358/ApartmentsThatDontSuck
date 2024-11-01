# Generated by Django 4.2.4 on 2024-07-17 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0034_rename_purchase_datetime_ticketpurchase_purchase_button_click_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketlisting',
            name='status',
            field=models.CharField(choices=[('Live', 'Live'), ('Cancelled', 'Cancelled - Listing taken down by seller'), ('Listed - Verif. Hold', 'Listed - hold for ticket verification by seller'), ('Listed - Verif. Expired', 'Listed - Seller failed to verify ticket in time'), ('On Hold - Reported Hold', 'On Hold - Hold due to listing reported'), ('Force Removed', 'Removed by staff due to violation of policy'), ('Sold - Awaiting Transfer', 'Sold - Awaiting ticket transfer'), ('Sold - Awaiting Payment Transfer to Seller', 'Sold - Awaiting Payment Transfer to Seller'), ('Sold', 'Ticket sold successfully'), ('Unsold', 'Ticket not sold before event start time')], max_length=50),
        ),
        migrations.AlterField(
            model_name='ticketpurchase',
            name='status',
            field=models.CharField(choices=[('Ticket(s) in Cart', 'Ticket(s) in Cart'), ('Sold - Awaiting Buyer Transfer Details', 'Sold - Awaiting Buyer Transfer Details'), ('Sold - Awaiting Ticket Transfer', 'Sold - Awaiting Ticket Transfer'), ('Sold - Awaiting Payment Transfer to Seller', 'Sold - Awaiting Payment Transfer to Seller'), ('Voided by Customer Service', 'Voided by Customer Service'), ('Cancelled - Items no longer Available', 'Cancelled - Items no longer Available'), ('Cancelled by Seller', 'Cancelled by Seller'), ('Sold - Finalized', 'Sold - Finalized')], max_length=50),
        ),
    ]
