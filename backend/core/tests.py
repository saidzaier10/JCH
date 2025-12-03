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
