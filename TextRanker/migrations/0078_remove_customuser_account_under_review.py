# Generated by Django 4.2.4 on 2024-09-11 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0077_search_live_search'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='account_under_review',
        ),
    ]
