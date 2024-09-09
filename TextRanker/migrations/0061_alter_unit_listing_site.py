# Generated by Django 4.2.4 on 2024-08-31 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0060_unit_neighborhood'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='listing_site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='TextRanker.listingsite'),
        ),
    ]