from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Member, Registration
from dateutil.relativedelta import relativedelta
import uuid

class Command(BaseCommand):
    help = 'Anonymise les adhérents inactifs depuis plus de 2 ans (Règle N+2)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simule l\'anonymisation sans modifier la base de données',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        # Date limite : il y a 2 ans
        cutoff_date = timezone.now().date() - relativedelta(years=2)
        
        self.stdout.write(f"Date limite de rétention : {cutoff_date}")

        # Récupérer tous les membres
        members = Member.objects.all()
        members_to_anonymize = []

        for member in members:
            # Ignorer si déjà anonymisé
            if member.last_name == "ANONYME":
                continue

            # Trouver la dernière inscription (basée sur la date de fin de la saison)
            last_registration = Registration.objects.filter(member=member).select_related('season').order_by('-season__end_date').first()

            if last_registration:
                last_activity_date = last_registration.season.end_date
            else:
                # Si aucune inscription, on se base sur la date de création du membre
                last_activity_date = member.created_at.date()

            if last_activity_date < cutoff_date:
                members_to_anonymize.append((member, last_activity_date))

        self.stdout.write(f"Nombre de membres inactifs trouvés : {len(members_to_anonymize)}")

        for member, last_date in members_to_anonymize:
            if dry_run:
                self.stdout.write(self.style.WARNING(f"[DRY RUN] Anonymisation de {member} (Dernière activité : {last_date})"))
            else:
                # Anonymisation
                original_name = str(member)
                member.first_name = "Anonyme"
                member.last_name = "ANONYME"
                member.email = ""
                member.phone = ""
                member.address = ""
                member.license_number = None
                member.has_passport = False
                member.birth_date = "1900-01-01" # Date fictive
                
                # Suppression des fichiers
                if member.photo:
                    member.photo.delete(save=False)
                if member.medical_certificate:
                    member.medical_certificate.delete(save=False)
                
                member.save()
                
                # Gestion du compte parent (User)
                if member.parent:
                    parent_user = member.parent
                    # Vérifier si ce parent a d'autres enfants NON anonymisés
                    other_children = Member.objects.filter(parent=parent_user).exclude(last_name="ANONYME")
                    if not other_children.exists():
                        # Anonymiser le parent aussi
                        parent_user.username = f"anonyme_{uuid.uuid4()}"
                        parent_user.email = ""
                        parent_user.first_name = ""
                        parent_user.last_name = ""
                        parent_user.is_active = False
                        parent_user.save()
                        self.stdout.write(f"  -> Compte parent désactivé et anonymisé")

                self.stdout.write(self.style.SUCCESS(f"Anonymisation de {original_name} effectuée."))

        if dry_run:
            self.stdout.write(self.style.SUCCESS("Fin de la simulation. Aucune donnée modifiée."))
        else:
            self.stdout.write(self.style.SUCCESS("Nettoyage terminé."))
