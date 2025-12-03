from django.core.management.base import BaseCommand
from core.models import Season, Category
from datetime import date

class Command(BaseCommand):
    help = 'Populate Judo Categories for 2025-2026'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating categories...")

        # 1. Create Season 2025-2026
        season, created = Season.objects.get_or_create(
            name="2025-2026",
            defaults={
                'start_date': date(2025, 9, 1),
                'end_date': date(2026, 6, 30),
                'is_active': True
            }
        )
        if not created:
            season.is_active = True
            season.save()
        
        self.stdout.write(f"Season: {season}")

        # 2. Define Categories (Reference Year: 2025)
        # Age = 2025 - BirthYear
        categories_data = [
            {"name": "Baby Judo", "code": "BABY", "age_min": 3, "age_max": 3, "price": 150},      # 2022
            {"name": "Eveils Judo", "code": "EVEIL", "age_min": 4, "age_max": 5, "price": 160},    # 2020-2021
            {"name": "Mini-Poussins", "code": "MINI", "age_min": 6, "age_max": 7, "price": 170},  # 2018-2019
            {"name": "Poussins", "code": "POUSSIN", "age_min": 8, "age_max": 9, "price": 180},     # 2016-2017
            {"name": "Benjamins", "code": "BENJAMIN", "age_min": 10, "age_max": 11, "price": 190}, # 2014-2015
            {"name": "Minimes", "code": "MINIME", "age_min": 12, "age_max": 13, "price": 200},     # 2012-2013
            {"name": "Cadets", "code": "CADET", "age_min": 14, "age_max": 16, "price": 210},       # 2009-2011
            {"name": "Juniors", "code": "JUNIOR", "age_min": 17, "age_max": 19, "price": 220},     # 2006-2008
            {"name": "Seniors", "code": "SENIOR", "age_min": 20, "age_max": 29, "price": 230},     # 2005 et avant (approx limit for Seniors vs Vets)
            {"name": "Vétérans", "code": "VETERAN", "age_min": 30, "age_max": 99, "price": 230},   # 1995 et avant
        ]

        for cat_data in categories_data:
            category, created = Category.objects.update_or_create(
                code=cat_data['code'],
                defaults={
                    'name': cat_data['name'],
                    'age_min': cat_data['age_min'],
                    'age_max': cat_data['age_max'],
                    'price': cat_data['price']
                }
            )
            self.stdout.write(f"Category: {category} (Age: {category.age_min}-{category.age_max})")

        self.stdout.write(self.style.SUCCESS("Categories populated successfully!"))
