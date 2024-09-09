from django.core.management.base import BaseCommand
from TextRanker.models import Neighborhood

class Command(BaseCommand):
    help = 'Add all Chicago neighborhoods to the Neighborhood model'

    def handle(self, *args, **kwargs):
        neighborhoods = [
            {"name": "Lincoln Park", "desirability": 9},
            {"name": "Wicker Park", "desirability": 8},
            {"name": "Hyde Park", "desirability": 5},
            {"name": "Lakeview", "desirability": 8},
            {"name": "River North", "desirability": 8},
            {"name": "Gold Coast", "desirability": 7},
            {"name": "South Loop", "desirability": 5},
            {"name": "West Loop", "desirability": 8},
            {"name": "Logan Square", "desirability": 7},
            {"name": "Old Town", "desirability": 8},
            {"name": "Streeterville", "desirability": 8},
            {"name": "Uptown", "desirability": 5},
            {"name": "Rogers Park", "desirability": 4},
            {"name": "Edgewater", "desirability": 5},
            {"name": "Chinatown", "desirability": 4},
            {"name": "Pilsen", "desirability": 6},
            {"name": "Andersonville", "desirability": 6},
            {"name": "Avondale", "desirability": 3},
            {"name": "Albany Park", "desirability": 5},
            {"name": "Bridgeport", "desirability": 4},
            {"name": "Lincoln Square/Ravenswood", "desirability": 5},
            {"name": "Humboldt Park", "desirability": 3},
            {"name": "Little Italy", "desirability": 6},
            {"name": "North Center", "desirability": 6},
            {"name": "Roscoe Village", "desirability": 6},
        ]

        for neighborhood in neighborhoods:
            obj, created = Neighborhood.objects.get_or_create(name=neighborhood['name'], defaults={'desirability': neighborhood['desirability']})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added {neighborhood['name']}"))
            else:
                self.stdout.write(self.style.WARNING(f"{neighborhood['name']} already exists"))

        self.stdout.write(self.style.SUCCESS('Successfully added all Chicago neighborhoods'))
