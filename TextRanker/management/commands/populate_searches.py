import csv
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from TextRanker.models import UnitType, ListingSite, Search
import os
from django.utils import timezone

class Command(BaseCommand):
    help = 'Add apartment searches to the model from a CSV file'

    def handle(self, *args, **kwargs):
        script_dir = os.path.dirname(__file__)
        csv_file_path = os.path.join(script_dir, 'apartmentsearches.csv')

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                unit_type_name = row['Unit Type']
                site_name = row['Site']
                search_url = row['URL']

                # Get or create UnitType
                unit_type, _ = UnitType.objects.get_or_create(unitType=unit_type_name)

                # Get or create ListingSite
                listing_site, _ = ListingSite.objects.get_or_create(site_name=site_name)

                if Search.objects.filter(
                    listing_site=listing_site,
                    unitType=unit_type
                ).exists():
                    self.stdout.write(self.style.NOTICE(f'Search for {search_url} already exists'))
                else:
                    # Create Search entry if it does not already exist
                    search = Search(
                        listing_site=listing_site,
                        search_url=search_url,
                        unitType=unit_type,
                        last_updated = timezone.now(),
                        last_item_note = 'None'
                    )
                    search.save()
                    self.stdout.write(self.style.SUCCESS(f'Added search for {search_url}'))

        self.stdout.write(self.style.SUCCESS('Finished processing CSV file.'))
