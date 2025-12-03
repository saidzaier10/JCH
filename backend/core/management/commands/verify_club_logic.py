from django.core.management.base import BaseCommand
from core.models import Season, Category, Member, Registration
from communications.models import EmailTemplate, EmailLog
from django.utils import timezone
from datetime import date

class Command(BaseCommand):
    help = 'Verify Club Management Logic'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting verification...")

        # 1. Create Season
        season, created = Season.objects.get_or_create(
            name="2024-2025",
            defaults={
                'start_date': date(2024, 9, 1),
                'end_date': date(2025, 6, 30),
                'is_active': True
            }
        )
        self.stdout.write(f"Season: {season}")

        # 2. Create Category
        category, created = Category.objects.get_or_create(
            code="U10",
            defaults={
                'name': "Poussins",
                'price': 150.00,
                'birth_year_min': 2014,
                'birth_year_max': 2015
            }
        )
        self.stdout.write(f"Category: {category}")

        # 3. Create Member
        member, created = Member.objects.get_or_create(
            email="test@example.com",
            defaults={
                'first_name': "Jean",
                'last_name': "Dupont",
                'birth_date': date(2014, 5, 15),
                'gender': 'M'
            }
        )
        self.stdout.write(f"Member: {member}")

        # 4. Register Member
        registration, created = Registration.objects.get_or_create(
            member=member,
            season=season,
            defaults={
                'category': category,
                'status': 'PENDING'
            }
        )
        self.stdout.write(f"Registration: {registration}")

        # 5. Create Email Template
        template, created = EmailTemplate.objects.get_or_create(
            key="WELCOME",
            defaults={
                'subject': "Bienvenue au Club",
                'body': "Bonjour {{ name }}, bienvenue !"
            }
        )
        self.stdout.write(f"Template: {template}")

        # 6. Create Email Log (Simulate sending)
        log = EmailLog.objects.create(
            recipient=member.email,
            subject=template.subject,
            status='SENT'
        )
        self.stdout.write(f"Email Log: {log}")

        self.stdout.write(self.style.SUCCESS("Verification completed successfully!"))
