# Generated by Django 4.2.4 on 2024-07-14 22:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('TextRanker', '0019_ticket_ticket_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]