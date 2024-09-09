# Generated by Django 4.2.4 on 2024-07-17 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0033_alter_ticketlisting_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketpurchase',
            old_name='purchase_datetime',
            new_name='purchase_button_click_datetime',
        ),
        migrations.AddField(
            model_name='ticketpurchase',
            name='payment_transferred_to_seller_datetime',
            field=models.DateTimeField(blank=True, help_text='Time payment was released to the seller.', null=True),
        ),
        migrations.AlterField(
            model_name='ticketpurchase',
            name='status',
            field=models.CharField(choices=[('Ticket(s) in Cart', 'Ticket(s) in Cart'), ('Sold - Awaiting Buyer Transfer Details', 'Sold - Awaiting Buyer Transfer Details'), ('Sold - Awaiting Ticket Transfer', 'Sold - Awaiting Ticket Transfer'), ('Sold - Awaiting Payment Transfer to Seller', 'Sold - Awaiting Payment Transfer to Seller'), ('Voided by Customer Service', 'Voided by Customer Service'), ('Cancelled by Seller', 'Cancelled by Seller'), ('Sold - Finalized', 'Sold - Finalized')], max_length=50),
        ),
    ]