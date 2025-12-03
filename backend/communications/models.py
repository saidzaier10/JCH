from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel

class EmailTemplate(TimeStampedModel):
    """
    Modèle pour les templates d'emails.
    """
    key = models.CharField(_("Clé unique"), max_length=50, unique=True, help_text=_("Identifiant unique pour le code (ex: WELCOME)"))
    subject = models.CharField(_("Sujet"), max_length=200)
    body = models.TextField(_("Contenu"), help_text=_("Contenu HTML ou Texte"))
    
    class Meta:
        verbose_name = _("Modèle d'email")
        verbose_name_plural = _("Modèles d'emails")

    def __str__(self):
        return f"{self.key} - {self.subject}"

class EmailLog(TimeStampedModel):
    """
    Log des emails envoyés.
    """
    STATUS_CHOICES = [
        ('SENT', _('Envoyé')),
        ('FAILED', _('Échoué')),
    ]

    recipient = models.EmailField(_("Destinataire"))
    subject = models.CharField(_("Sujet"), max_length=200)
    status = models.CharField(_("Statut"), max_length=20, choices=STATUS_CHOICES)
    error_message = models.TextField(_("Message d'erreur"), blank=True)

    class Meta:
        verbose_name = _("Log Email")
        verbose_name_plural = _("Logs Emails")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.recipient} - {self.subject} ({self.status})"
