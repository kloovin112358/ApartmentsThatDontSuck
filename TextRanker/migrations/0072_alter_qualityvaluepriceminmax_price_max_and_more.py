# Generated by Django 4.2.4 on 2024-09-03 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0071_alter_qualityvaluepriceminmax_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualityvaluepriceminmax',
            name='price_max',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='qualityvaluepriceminmax',
            name='price_min',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
