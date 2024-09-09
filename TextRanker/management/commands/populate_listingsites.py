from django.core.management.base import BaseCommand
from TextRanker.models import ListingSite

class Command(BaseCommand):
    help = 'Add listing sites to the ListingSite model'

    def handle(self, *args, **kwargs):
        sites = [
            "Apartments.com",
            "ApartmentGuide",
            "ForRent.com",
            "Domu",
            "Redfin",
            "Rent.com",
            "Craigslist",
            "Compass",
            "ApartmentAdvisor",
            "Facebook Marketplace",
            "Realtor.com",
            "HotPads",
            "Zillow",
            "Padmapper",
            "Zumper"
        ]

        for site in sites:
            obj, created = ListingSite.objects.get_or_create(site_name=site)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added {site}"))
            else:
                self.stdout.write(self.style.WARNING(f"{site} already exists"))

        self.stdout.write(self.style.SUCCESS('Successfully added all listing sites'))
