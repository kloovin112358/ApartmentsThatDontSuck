from django.core.management.base import BaseCommand
from TextRanker.models import DisposableEmailDomain
import os

class Command(BaseCommand):
    help = 'Add disposable email domains to the DisposableEmailDomain model'

    def handle(self, *args, **kwargs):
        # Path to the file
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'disposableemaildomains.txt')

        # Read the file and process each line
        with open(file_path, 'r') as file:
            domains = file.readlines()
        
        # Process each domain
        for domain in domains:
            domain = domain.strip()  # Remove any leading/trailing whitespace

            # Check if domain already exists to avoid duplicates
            if not DisposableEmailDomain.objects.filter(domain=domain).exists():
                # Create and save new domain
                DisposableEmailDomain.objects.create(domain=domain)
                self.stdout.write(self.style.SUCCESS(f'Successfully added domain: {domain}'))
            else:
                self.stdout.write(self.style.WARNING(f'Domain already exists: {domain}'))