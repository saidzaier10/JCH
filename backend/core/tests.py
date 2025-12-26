from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone
from datetime import timedelta
from .models import Season, Category, Member

class SeasonConstraintTests(TestCase):
    def test_start_date_before_end_date(self):
        start = timezone.now().date()
        end = start + timedelta(days=30)
        season = Season(name="Test Season", start_date=start, end_date=end)
        season.full_clean()
        season.save()

    def test_start_date_after_end_date_fails(self):
        start = timezone.now().date()
        end = start - timedelta(days=1)
        season = Season(name="Bad Season", start_date=start, end_date=end)
        with self.assertRaises(ValidationError):
            season.full_clean()
        # Note: SQLite might not enforce CheckConstraint immediately on save without full_clean, 
        # but Postgres does. We test full_clean() for the validation logic.

class CategoryConstraintTests(TestCase):
    def test_age_min_lte_age_max(self):
        category = Category(name="Test Cat", code="TEST", price=100, age_min=10, age_max=12)
        category.full_clean()
        category.save()

    def test_age_min_gt_age_max_fails(self):
        category = Category(name="Bad Cat", code="BAD", price=100, age_min=12, age_max=10)
        with self.assertRaises(ValidationError):
            category.full_clean()

class MemberConstraintTests(TestCase):
    def test_birth_date_in_past(self):
        birth = timezone.now().date() - timedelta(days=365*10)
        member = Member(first_name="John", last_name="Doe", birth_date=birth)
        member.full_clean()
        member.save()

    def test_birth_date_in_future_fails(self):
        birth = timezone.now().date() + timedelta(days=1)
        member = Member(first_name="Future", last_name="Man", birth_date=birth)
        with self.assertRaises(ValidationError):
            member.full_clean()

from decimal import Decimal
from core.models import Registration
from core.services import PriceCalculator
from django.contrib.auth.models import User

class PriceCalculatorTest(TestCase):
    def setUp(self):
        self.parent = User.objects.create(username='parent', email='parent@test.com')
        self.season = Season.objects.create(name='2024-2025', start_date='2024-09-01', end_date='2025-06-30', is_active=True)
        self.category = Category.objects.create(name='Test Cat', code='TEST', price=Decimal('200.00'))
        
        self.member = Member.objects.create(
            first_name='Kid', last_name='Test', birth_date='2010-01-01', 
            gender='M', parent=self.parent, license_number='12345'
        )

    def test_standard_price(self):
        reg = Registration.objects.create(member=self.member, season=self.season, category=self.category)
        details = PriceCalculator.calculate_price(reg)
        self.assertEqual(details['final_price'], Decimal('200.00'))

    def test_supplementary_discipline(self):
        reg = Registration.objects.create(
            member=self.member, season=self.season, category=self.category,
            has_supplementary_discipline=True
        )
        details = PriceCalculator.calculate_price(reg)
        # 200 + 40 = 240
        self.assertEqual(details['final_price'], Decimal('240.00'))

    def test_city_hall_aid(self):
        reg = Registration.objects.create(
            member=self.member, season=self.season, category=self.category,
            city_hall_aid=True, city_hall_aid_amount=Decimal('50.00')
        )
        details = PriceCalculator.calculate_price(reg)
        # 200 - 50 = 150
        self.assertEqual(details['final_price'], Decimal('150.00'))

    def test_combined_supplement_and_aid(self):
        reg = Registration.objects.create(
            member=self.member, season=self.season, category=self.category,
            has_supplementary_discipline=True,
            city_hall_aid=True, city_hall_aid_amount=Decimal('50.00')
        )
        details = PriceCalculator.calculate_price(reg)
        # 200 + 40 - 50 = 190
        self.assertEqual(details['final_price'], Decimal('190.00'))

    def test_manual_discount(self):
        reg = Registration.objects.create(
            member=self.member, season=self.season, category=self.category,
            discount_amount=Decimal('20.00')
        )
        details = PriceCalculator.calculate_price(reg)
        # 200 - 20 = 180
        self.assertEqual(details['final_price'], Decimal('180.00'))
