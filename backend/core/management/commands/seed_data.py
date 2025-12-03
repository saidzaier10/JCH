import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker
from core.models import Season, Category, Member, Registration
from content.models import Event, Convocation

fake = Faker('fr_FR')

class Command(BaseCommand):
    help = 'Seed the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Create Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'password123')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created'))

        # 2. Create Season
        season, created = Season.objects.get_or_create(
            name='2024-2025',
            defaults={
                'start_date': date(2024, 9, 1),
                'end_date': date(2025, 6, 30),
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Season "{season.name}" created'))

        # 3. Create Categories
        categories_data = [
            {'name': 'Eveil Judo', 'code': 'EVEIL', 'price': 180, 'age_min': 4, 'age_max': 5},
            {'name': 'Mini-Poussins', 'code': 'MINI', 'price': 190, 'age_min': 6, 'age_max': 7},
            {'name': 'Poussins', 'code': 'POUSSIN', 'price': 200, 'age_min': 8, 'age_max': 9},
            {'name': 'Benjamins', 'code': 'BENJAMIN', 'price': 210, 'age_min': 10, 'age_max': 11},
            {'name': 'Minimes', 'code': 'MINIME', 'price': 220, 'age_min': 12, 'age_max': 13},
            {'name': 'Cadets', 'code': 'CADET', 'price': 230, 'age_min': 14, 'age_max': 16},
            {'name': 'Juniors/Seniors', 'code': 'ADULTE', 'price': 240, 'age_min': 17, 'age_max': 99},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, _ = Category.objects.get_or_create(
                code=cat_data['code'],
                defaults=cat_data
            )
            categories.append(category)
        self.stdout.write(self.style.SUCCESS(f'{len(categories)} categories created/checked'))

        # 4. Create Parents (Users) and Members (Children)
        for _ in range(10):
            # Create Parent
            username = fake.user_name()
            email = fake.email()
            if not User.objects.filter(username=username).exists():
                parent = User.objects.create_user(username=username, email=email, password='password123')
                parent.first_name = fake.first_name()
                parent.last_name = fake.last_name()
                parent.save()

                # Create 1 to 3 children per parent
                for _ in range(random.randint(1, 3)):
                    gender = random.choice(['M', 'F'])
                    first_name = fake.first_name_male() if gender == 'M' else fake.first_name_female()
                    birth_date = fake.date_of_birth(minimum_age=4, maximum_age=18)
                    
                    member = Member.objects.create(
                        parent=parent,
                        first_name=first_name,
                        last_name=parent.last_name,
                        birth_date=birth_date,
                        gender=gender,
                        address=fake.address(),
                        has_passport=random.choice([True, False]),
                        license_number=fake.bothify(text='??######')
                    )

                    # Register member to season
                    # Find suitable category based on age
                    age = 2025 - birth_date.year
                    suitable_category = next((c for c in categories if c.age_min <= age <= c.age_max), categories[-1])

                    Registration.objects.create(
                        member=member,
                        season=season,
                        category=suitable_category,
                        status=random.choice(['VALIDATED', 'PENDING', 'VALIDATED', 'VALIDATED']), # Mostly validated
                        paid=random.choice([True, False])
                    )

        self.stdout.write(self.style.SUCCESS('10 Families with children and registrations created'))

        # 5. Create Events
        events_data = [
            {'title': 'Tournoi de Rentrée', 'type': 'COMPETITION', 'delta_days': 15},
            {'title': 'Stage Toussaint', 'type': 'TRAINING', 'delta_days': 45},
            {'title': 'Coupe de Noël', 'type': 'COMPETITION', 'delta_days': 90},
            {'title': 'Interclubs Régional', 'type': 'COMPETITION', 'delta_days': 120},
        ]

        for event_data in events_data:
            start_time = timezone.now() + timedelta(days=event_data['delta_days'])
            end_time = start_time + timedelta(hours=4)
            
            Event.objects.create(
                title=event_data['title'],
                description=fake.text(),
                start_time=start_time,
                end_time=end_time,
                location=fake.city(),
                type=event_data['type']
            )
        
        self.stdout.write(self.style.SUCCESS('Events created'))
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
