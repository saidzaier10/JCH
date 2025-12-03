from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel

class Event(TimeStampedModel):
    """
    Modèle représentant un événement du club (compétition, stage, etc.).
    """
    EVENT_TYPES = [
        ('COMPETITION', _('Compétition')),
        ('TRAINING', _('Stage')),
        ('OTHER', _('Autre')),
    ]

    title = models.CharField(_("Titre"), max_length=200)
    description = models.TextField(_("Description"))
    start_time = models.DateTimeField(_("Date de début"))
    end_time = models.DateTimeField(_("Date de fin"))
    location = models.CharField(_("Lieu"), max_length=200, blank=True)
    type = models.CharField(_("Type"), max_length=20, choices=EVENT_TYPES, default='OTHER')

    class Meta:
        verbose_name = _("Événement")
        verbose_name_plural = _("Événements")
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['start_time']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F('end_time')),
                name='event_start_time_before_end_time'
            )
        ]

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError(_("La date de début doit être antérieure à la date de fin."))
        super().clean()

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"

class Convocation(TimeStampedModel):
    """
    Modèle représentant une convocation d'un adhérent à un événement.
    """
    STATUS_CHOICES = [
        ('PENDING', _('En attente')),
        ('SENT', _('Envoyée')),
        ('CONFIRMED', _('Confirmée')),
        ('DECLINED', _('Refusée')),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='convocations', verbose_name=_("Événement"))
    member = models.ForeignKey('core.Member', on_delete=models.CASCADE, related_name='convocations', verbose_name=_("Adhérent"))
    status = models.CharField(_("Statut"), max_length=20, choices=STATUS_CHOICES, default='PENDING')
    sent_at = models.DateTimeField(_("Envoyée le"), null=True, blank=True)

    class Meta:
        verbose_name = _("Convocation")
        verbose_name_plural = _("Convocations")
        unique_together = ['event', 'member']
        indexes = [
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Convocation {self.member} - {self.event}"

class GalleryImage(models.Model):
    """
    Modèle représentant une image de la galerie photo.
    """
    CATEGORY_CHOICES = [
        ('EVENT', _('Événement')),
        ('COMPETITION', _('Compétition')),
        ('INTERNSHIP', _('Stage')),
        ('OTHER', _('Autre')),
    ]

    title = models.CharField(_("Titre"), max_length=200, blank=True)
    image = models.ImageField(_("Image"), upload_to='gallery/')
    category = models.CharField(_("Catégorie"), max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    uploaded_at = models.DateTimeField(_("Date d'ajout"), auto_now_add=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Galerie Photos")
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['uploaded_at']),
        ]

    def __str__(self):
        return self.title or f"Image {self.id}"
