# Generated by Django 4.2.4 on 2024-07-26 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0048_ticketlisting_age_restriction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venue',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='longitude',
        ),
        migrations.AlterField(
            model_name='ticketlisting',
            name='original_purchase_location',
            field=models.ForeignKey(help_text='What platform hosts your ticket(s)? This is most likely the website from which you purchased your tickets.', on_delete=django.db.models.deletion.RESTRICT, to='TextRanker.ticketoriginalpurchaselocation', verbose_name='Ticket Vendor'),
        ),
    ]
