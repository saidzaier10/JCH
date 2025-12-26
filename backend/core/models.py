from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class TimeStampedModel(models.Model):
    """
    Modèle abstrait ajoutant les champs de traçabilité temporelle.
    """
    created_at = models.DateTimeField(_("Date de création"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Dernière modification"), auto_now=True)

    class Meta:
        abstract = True

class PaymentOption(TimeStampedModel):
    """
    Modèle représentant une option de paiement (ex: 3 fois sans frais).
    """
    name = models.CharField(_("Nom"), max_length=100)
    installments = models.IntegerField(_("Nombre d'échéances"), default=1)
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Option de paiement")
        verbose_name_plural = _("Options de paiement")

    def __str__(self):
        return f"{self.name} ({self.installments} échéances)"

class Season(TimeStampedModel):
    """
    Modèle représentant une saison sportive (ex: 2024-2025).
    """
    name = models.CharField(_("Nom"), max_length=50, unique=True)
    start_date = models.DateField(_("Date de début"))
    end_date = models.DateField(_("Date de fin"))
    is_active = models.BooleanField(_("Active"), default=False)

    class Meta:
        verbose_name = _("Saison")
        verbose_name_plural = _("Saisons")
        ordering = ['-start_date']
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__lt=models.F('end_date')),
                name='season_start_date_before_end_date'
            )
        ]

    def __str__(self):
        return self.name

    def clean(self):
        """
        Validation personnalisée.
        Vérifie que la date de début est bien avant la date de fin.
        """
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError(_("La date de début doit être antérieure à la date de fin."))
        super().clean()

    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour gérer la contrainte d'unicité de la saison active.
        Si la saison courante est active, on désactive toutes les autres.
        """
        if self.is_active:
            # Désactiver les autres saisons si celle-ci est active
            Season.objects.exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)


class Category(TimeStampedModel):
    """
    Modèle représentant une catégorie d'âge/niveau (ex: U10, Seniors).
    """
    name = models.CharField(_("Nom"), max_length=50)
    code = models.CharField(_("Code"), max_length=20, unique=True)
    description = models.TextField(_("Description"), blank=True)
    price = models.DecimalField(_("Prix de la cotisation"), max_digits=6, decimal_places=2)
    age_min = models.IntegerField(_("Âge minimum"), null=True, blank=True)
    age_max = models.IntegerField(_("Âge maximum"), null=True, blank=True)

    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")
        constraints = [
            models.CheckConstraint(
                check=models.Q(age_min__lte=models.F('age_max')),
                name='category_age_min_lte_age_max'
            )
        ]

    def clean(self):
        """
        Vérifie la cohérence des âges (min <= max).
        """
        if self.age_min is not None and self.age_max is not None and self.age_min > self.age_max:
            raise ValidationError(_("L'âge minimum doit être inférieur ou égal à l'âge maximum."))
        super().clean()

    def __str__(self):
        return f"{self.name} ({self.price}€)"


class Member(TimeStampedModel):
    """
    Modèle représentant un adhérent du club.
    """
    GENDER_CHOICES = [
        ('M', _('Masculin')),
        ('F', _('Féminin')),
    ]

    WEIGHT_CHOICES = [
        # Eveil / Mini-Poussins / Poussins
        ('-20', '-20 kg'), ('-23', '-23 kg'), ('-26', '-26 kg'), ('-29', '-29 kg'),
        ('+29', '+29 kg'), ('-32', '-32 kg'), ('-35', '-35 kg'), ('+46', '+46 kg'),
        # Benjamins
        ('-28', '-28 kg'), ('-30', '-30 kg'), ('-34', '-34 kg'), ('-38', '-38 kg'),
        ('-42', '-42 kg'), ('-46', '-46 kg'), ('-50', '-50 kg'), ('-55', '-55 kg'),
        ('-60', '-60 kg'), ('-66', '-66 kg'), ('+66', '+66 kg'), ('+63', '+63 kg'),
        # Minimes / Cadets / Juniors / Seniors
        ('-36', '-36 kg'), ('-40', '-40 kg'), ('-44', '-44 kg'), ('-48', '-48 kg'),
        ('-52', '-52 kg'), ('-57', '-57 kg'), ('-63', '-63 kg'), ('-70', '-70 kg'),
        ('-73', '-73 kg'), ('-78', '-78 kg'), ('-81', '-81 kg'), ('-90', '-90 kg'),
        ('-100', '-100 kg'), ('+70', '+70 kg'), ('+73', '+73 kg'), ('+78', '+78 kg'),
        ('-100', '-100 kg'), ('+70', '+70 kg'), ('+73', '+73 kg'), ('+78', '+78 kg'),
        ('+90', '+90 kg'), ('+100', '+100 kg'),
    ]

    DISCIPLINE_CHOICES = [
        ('EVEIL', _('Judo Éveil')),
        ('JUDO', _('Judo')),
        ('TAISO', _('Taïso')),
        ('TAISO_SENIOR', _('Taïso Senior')),
        ('APA', _('Activité Physique Adaptée')),
        ('JUJITSU', _('Ju-Jitsu')),
    ]

    BELT_CHOICES = [
        ('WHITE', _('Blanche')),
        ('WHITE_YELLOW', _('Blanche-Jaune')),
        ('YELLOW', _('Jaune')),
        ('YELLOW_ORANGE', _('Jaune-Orange')),
        ('ORANGE', _('Orange')),
        ('ORANGE_GREEN', _('Orange-Verte')),
        ('GREEN', _('Verte')),
        ('BLUE', _('Bleue')),
        ('BROWN', _('Marron')),
        ('BLACK', _('Noire')),
    ]

    parent = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name=_("Parent"))
    first_name = models.CharField(_("Prénom"), max_length=100)
    last_name = models.CharField(_("Nom"), max_length=100)
    email = models.EmailField(_("Email"), blank=True) # Removed unique=True
    phone = models.CharField(_("Téléphone"), max_length=20, blank=True)
    birth_date = models.DateField(_("Date de naissance"))
    gender = models.CharField(_("Genre"), max_length=1, choices=GENDER_CHOICES, default='M')
    address = models.TextField(_("Adresse"), blank=True)
    license_number = models.CharField(_("Numéro de licence"), max_length=50, unique=True, blank=True, null=True)
    has_passport = models.BooleanField(_("Passeport Judo"), default=False)
    photo = models.ImageField(_("Photo"), upload_to='members/photos/', blank=True, null=True)
    medical_certificate = models.FileField(_("Certificat médical"), upload_to='members/medical/', blank=True, null=True)
    medical_certificate_valid_until = models.DateField(_("Validité certificat"), null=True, blank=True)
    weight_category = models.CharField(_("Catégorie de poids"), max_length=10, choices=WEIGHT_CHOICES, blank=True, null=True)
    discipline = models.CharField(_("Discipline principale"), max_length=20, choices=DISCIPLINE_CHOICES, default='JUDO')
    belt = models.CharField(_("Ceinture actuelle"), max_length=20, choices=BELT_CHOICES, default='WHITE')
    image_rights = models.BooleanField(_("Droit à l'image"), default=False, help_text=_("J'autorise le club à utiliser mon image dans le cadre de sa communication."))

    class Meta:
        verbose_name = _("Adhérent")
        verbose_name_plural = _("Adhérents")
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['last_name']),
        ]

    def clean(self):
        """
        Vérifie que la date de naissance n'est pas dans le futur.
        """
        if self.birth_date and self.birth_date > timezone.now().date():
            raise ValidationError(_("La date de naissance ne peut pas être dans le futur."))
        super().clean()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Registration(TimeStampedModel):
    """
    Modèle représentant l'inscription d'un membre à une saison et une catégorie.
    """
    STATUS_CHOICES = [
        ('PENDING', _('En attente')),
        ('VALIDATED', _('Validée')),
        ('REJECTED', _('Rejetée')),
    ]

    PAYMENT_MODE_CHOICES = [
        ('FULL', _('Comptant')),
        ('3X', _('3 Fois')),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='registrations', verbose_name=_("Adhérent"))
    season = models.ForeignKey(Season, on_delete=models.PROTECT, related_name='registrations', verbose_name=_("Saison"))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='registrations', verbose_name=_("Catégorie"))
    status = models.CharField(_("Statut"), max_length=20, choices=STATUS_CHOICES, default='PENDING')
    paid = models.BooleanField(_("Payé"), default=False)
    payment_date = models.DateField(_("Date de paiement"), null=True, blank=True)
    payment_mode = models.CharField(_("Mode de paiement (Legacy)"), max_length=10, choices=PAYMENT_MODE_CHOICES, default='FULL', blank=True, null=True)
    payment_option = models.ForeignKey(PaymentOption, on_delete=models.SET_NULL, null=True, blank=True, related_name='registrations', verbose_name=_("Option de paiement"))
    installments_paid = models.IntegerField(_("Mensualités payées"), default=0) # 0, 1, 2, or 3
    discount_percentage = models.DecimalField(_("Remise manuelle (%)"), max_digits=5, decimal_places=2, default=0.0)
    discount_amount = models.DecimalField(_("Remise manuelle (€)"), max_digits=6, decimal_places=2, default=0.0)
    city_hall_aid = models.BooleanField(_("Aide Mairie"), default=False)
    city_hall_aid_amount = models.DecimalField(_("Montant Aide Mairie"), max_digits=6, decimal_places=2, default=0.0)
    has_supplementary_discipline = models.BooleanField(_("Discipline supplémentaire (+40€)"), default=False)
    notes = models.TextField(_("Notes internes"), blank=True)

    class Meta:
        verbose_name = _("Inscription")
        verbose_name_plural = _("Inscriptions")
        unique_together = ['member', 'season']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['paid']),
        ]

    def __str__(self):
        return f"{self.member} - {self.season} - {self.category}"


class Invoice(TimeStampedModel):
    """
    Modèle représentant une facture pour un adhérent.
    """
    STATUS_CHOICES = [
        ('PENDING', _('En attente')),
        ('PAID', _('Payée')),
        ('CANCELLED', _('Annulée')),
    ]

    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='invoices', verbose_name=_("Inscription"), null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='invoices', verbose_name=_("Adhérent"))
    amount = models.DecimalField(_("Montant"), max_digits=10, decimal_places=2)
    date_issued = models.DateField(_("Date d'émission"))
    status = models.CharField(_("Statut"), max_length=20, choices=STATUS_CHOICES, default='PENDING')
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("Facture")
        verbose_name_plural = _("Factures")
        indexes = [
            models.Index(fields=['date_issued']),
            models.Index(fields=['status']),
        ]

    def clean(self):
        """
        Vérifie la cohérence entre l'inscription et l'adhérent facturé.
        """
        if self.registration and self.member != self.registration.member:
            raise ValidationError(_("L'adhérent de la facture doit correspondre à l'adhérent de l'inscription."))
        super().clean()

    def __str__(self):
        return f"Facture #{self.id} - {self.member} - {self.amount}€"
