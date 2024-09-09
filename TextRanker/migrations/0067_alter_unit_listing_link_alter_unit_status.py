# Generated by Django 4.2.4 on 2024-09-03 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0066_contactformmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='listing_link',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='status',
            field=models.CharField(choices=[('Live', 'Live'), ('Sold', 'Sold'), ('Sucks', 'Sucks')], max_length=10),
        ),
    ]