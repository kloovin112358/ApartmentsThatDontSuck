# Generated by Django 4.2.4 on 2024-09-01 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0063_alter_emailverification_verified_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]
