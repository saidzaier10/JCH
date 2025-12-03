from django.db import models
from core.models import Member

class Course(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    )

    name = models.CharField(max_length=100)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_day_of_week_display()})"

class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('course', 'date')

    def __str__(self):
        return f"{self.course.name} - {self.date}"

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('PRESENT', 'Présent'),
        ('ABSENT', 'Absent'),
        ('EXCUSED', 'Excusé'),
    )

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendances')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PRESENT')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'member')

    def __str__(self):
        return f"{self.member} - {self.session} - {self.status}"
