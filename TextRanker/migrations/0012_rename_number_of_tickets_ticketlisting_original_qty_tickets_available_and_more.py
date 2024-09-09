# Generated by Django 4.2.4 on 2024-07-13 00:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0011_ticketlisting_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketlisting',
            old_name='number_of_tickets',
            new_name='original_qty_tickets_available',
        ),
        migrations.AddField(
            model_name='ticketlisting',
            name='current_qty_tickets_available',
            field=models.PositiveSmallIntegerField(default=1, help_text='How many tickets are still left?', validators=[django.core.validators.MaxValueValidator(10)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticketpurchase',
            name='qty_purchased',
            field=models.PositiveSmallIntegerField(default=1, help_text='How many tickets were purchased?', validators=[django.core.validators.MaxValueValidator(10)]),
            preserve_default=False,
        ),
    ]