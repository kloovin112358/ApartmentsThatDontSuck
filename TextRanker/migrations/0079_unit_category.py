# Generated by Django 4.2.4 on 2024-09-16 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0078_remove_customuser_account_under_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='category',
            field=models.CharField(choices=[('Frugal', 'Frugal'), ('Value', 'Value'), ('Dream', 'Dream')], default='Value', max_length=6),
        ),
    ]
