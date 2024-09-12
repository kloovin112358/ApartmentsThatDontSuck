from django.core.management.base import BaseCommand
from TextRanker.models import UnitType

class Command(BaseCommand):
    help = 'Add unit types to the UnitType model'

    def handle(self, *args, **kwargs):
        unit_types = [
            "Studio",
            "1-Bedroom",
            "2-Bedroom",
            "3-Bedroom",
        ]

        for unit_type in unit_types:
            obj, created = UnitType.objects.get_or_create(unitType=unit_type)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added {unit_type}"))
            else:
                self.stdout.write(self.style.WARNING(f"{unit_type} already exists"))

        self.stdout.write(self.style.SUCCESS('Successfully added all unit types'))
