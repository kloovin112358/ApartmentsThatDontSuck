# Generated by Django 4.2.4 on 2024-07-14 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0021_alter_ticket_ticket_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='TextRanker.ticketlisting'),
        ),
    ]
