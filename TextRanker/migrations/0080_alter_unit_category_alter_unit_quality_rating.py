# Generated by Django 4.2.4 on 2024-10-10 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0079_unit_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='category',
            field=models.CharField(blank=True, choices=[('Frugal', 'Frugal'), ('Value', 'Value'), ('Dream', 'Dream')], default='Value', max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='quality_rating',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
