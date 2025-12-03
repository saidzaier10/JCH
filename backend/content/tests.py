from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Event

class EventConstraintTests(TestCase):
    def test_start_time_before_end_time(self):
        start = timezone.now()
        end = start + timedelta(hours=2)
        event = Event(title="Test Event", description="Desc", start_time=start, end_time=end)
        event.full_clean()
        event.save()

    def test_start_time_after_end_time_fails(self):
        start = timezone.now()
        end = start - timedelta(hours=1)
        event = Event(title="Bad Event", description="Desc", start_time=start, end_time=end)
        with self.assertRaises(ValidationError):
            event.full_clean()
