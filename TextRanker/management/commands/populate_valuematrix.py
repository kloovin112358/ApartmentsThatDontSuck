from django.core.management.base import BaseCommand
from TextRanker.models import QualityRating, QualityValuePriceMinMax, QualityValue, UnitType

class Command(BaseCommand):
    help = 'Populate QualityRating, QualityValuePriceMinMax, and QualityValue models with predefined data.'

    def handle(self, *args, **kwargs):
        # Populate QualityRating
        for i in range(1, 11):
            QualityRating.objects.get_or_create(quality_rating=i)

        # Populate UnitType
        unit_types = ['Studio', '1-Bedroom', '2-Bedroom', '3-Bedroom']
        for unit_type in unit_types:
            UnitType.objects.get_or_create(unitType=unit_type)

        # Define price ranges for each unit type
        price_ranges = {
            'Studio': [
                (0, 800), (800, 1000), (1000, 1200), (1200, 1400), (1400, 1600),
                (1600, 1800), (1800, 2000), (2000, 999999)
            ],
            '1-Bedroom': [
                (0, 1000), (1000, 1200), (1200, 1400), (1400, 1600), (1600, 1800),
                (1800, 2100), (2100, 2600), (2600, 999999)
            ],
            '2-Bedroom': [
                (0, 1600), (1600, 2000), (2000, 2500), (2500, 3000), (3000, 3500),
                (3500, 4000), (4000, 5000), (5000, 999999)
            ],
            '3-Bedroom': [
                (0, 2000), (2000, 2300), (2300, 2600), (2600, 3000), (3000, 3500),
                (3500, 4000), (4000, 5000), (5000, 999999)
            ]
        }

        # Populate QualityValuePriceMinMax
        for unit_type in UnitType.objects.all():
            for min_price, max_price in price_ranges[unit_type.unitType]:
                QualityValuePriceMinMax.objects.get_or_create(
                    unit_type=unit_type,
                    price_min=min_price,
                    price_max=max_price
                )

        # Define value ratings for Studio
        value_ratings = {
            1: [1, 1, 1, 1, 1, 1, 2],
            2: [1, 1, 1, 1, 1, 2, 5],
            3: [1, 1, 1, 1, 2, 5, 8],
            4: [1, 1, 1, 2, 5, 8, 10],
            5: [1, 1, 8, 10, 5, 10, 10],
            6: [1, 3, 5, 8, 9, 10, 10],
            7: [3, 5, 7, 9, 10, 10, 10],
            8: [5, 6, 8, 9, 10, 10, 10],
            9: [6, 8, 9, 10, 10, 10, 10],
            10: [7, 9, 10, 10, 10, 10, 10]
        }

        # Populate QualityValue for each UnitType and QualityValuePriceMinMax
        for unit_type in UnitType.objects.all():
            for quality_rating in QualityRating.objects.all().order_by('quality_rating'):
                qvpmmCounter = 0
                for price_range in QualityValuePriceMinMax.objects.filter(unit_type=unit_type).order_by('price_min'):
                    value_rating = value_ratings[quality_rating.quality_rating][qvpmmCounter]
                    QualityValue.objects.get_or_create(
                        unit_type=unit_type,
                        quality_rating=quality_rating,
                        min_max=price_range,
                        value_rating=value_rating
                    )
                    qvpmmCounter += 1

        self.stdout.write(self.style.SUCCESS('Successfully populated QualityRating, QualityValuePriceMinMax, and QualityValue models.'))
