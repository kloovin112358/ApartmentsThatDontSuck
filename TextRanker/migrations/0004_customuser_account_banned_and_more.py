# Generated by Django 4.2.4 on 2024-07-12 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0003_disposableemaildomain_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='account_banned',
            field=models.BooleanField(default=False, help_text='If this is true, user has been banned for cause after review by admin'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='account_under_review',
            field=models.BooleanField(default=False, help_text='This will be true when a ticket listing by this user has been reported'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='ban_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date and time of account ban'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='verified_account',
            field=models.BooleanField(default=False, help_text='Flipped to true when user clicks verification link sent to email address', verbose_name='Verified account?'),
        ),
    ]
