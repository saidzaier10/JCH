from decimal import Decimal
from .models import Registration

class PriceCalculator:
    """
    Service pour calculer le prix d'une inscription en appliquant les réductions familiales.
    """
    
    @staticmethod
    def calculate_price(registration):
        """
        Calcule le prix final pour une inscription donnée.
        Règles (par défaut) :
        - 1er enfant : Plein tarif
        - 2ème enfant : -10%
        - 3ème enfant et + : -20%
        """
        category_price = registration.category.price
        
        # Récupérer les autres inscriptions de la même famille (même parent) pour la même saison
        # On exclut l'inscription actuelle si elle existe déjà
        siblings_registrations = Registration.objects.filter(
            member__parent=registration.member.parent,
            season=registration.season,
            status='VALIDATED' # On ne compte que les inscriptions validées ou en cours de paiement
        ).exclude(id=registration.id).order_by('created_at')
        
        count = siblings_registrations.count()
        
        # L'inscription actuelle est la (count + 1)ème
        rank = count + 1
        
        discount_percentage = Decimal('0.00')
        
        if rank == 2:
            discount_percentage = Decimal('0.10') # 10%
        elif rank >= 3:
            discount_percentage = Decimal('0.20') # 20%
            
        # Réductions familiales
        family_discount_amount = category_price * discount_percentage
        price_after_family_discount = category_price - family_discount_amount
        
        # Réductions manuelles (pourcentage)
        manual_discount_percent = Decimal(str(registration.discount_percentage)) / Decimal('100')
        manual_discount_amount_from_percent = price_after_family_discount * manual_discount_percent
        
        # Calcul prix final (prix de base - reduc famille - reduc manuelle % - reduc manuelle montant)
        final_price = price_after_family_discount - manual_discount_amount_from_percent - Decimal(str(registration.discount_amount))

        # Ajout Discipline Supplémentaire
        if registration.has_supplementary_discipline:
            final_price += Decimal('40.00')

        # Déduction Aide Mairie (Pass Sport / Chèques Vacances ...)
        if registration.city_hall_aid and registration.city_hall_aid_amount > 0:
            final_price -= Decimal(str(registration.city_hall_aid_amount))
        
        # Sécurité: Le prix ne peut pas être négatif
        if final_price < 0:
            final_price = Decimal('0.00')
        
        return {
            'base_price': category_price,
            'family_discount_percentage': discount_percentage * 100,
            'family_discount_amount': family_discount_amount,
            'manual_discount_percentage': registration.discount_percentage,
            'manual_discount_amount': registration.discount_amount,
            'supplements': Decimal('40.00') if registration.has_supplementary_discipline else Decimal('0.00'),
            'city_hall_aid_amount': registration.city_hall_aid_amount if registration.city_hall_aid else Decimal('0.00'),
            'final_price': final_price,
            'rank': rank
        }

    @staticmethod
    def get_payment_details(registration):
        """
        Calcule le total à payer, le montant déjà payé et le reste à payer.
        """
        price_data = PriceCalculator.calculate_price(registration)
        total_to_pay = price_data['final_price']
        
        amount_paid = Decimal('0.00')
        
        if registration.paid:
            amount_paid = total_to_pay
        elif registration.installments_paid > 0:
            # Mode Paiement en plusieurs fois (ex: 3X)
            # Logique simplifiée : Total / 3 * nombre de mensualités payées
            amount_paid = (total_to_pay / 3) * registration.installments_paid
        
        remaining_to_pay = total_to_pay - amount_paid
        
        if remaining_to_pay < 0:
            remaining_to_pay = Decimal('0.00')

        return {
            'total_to_pay': total_to_pay,
            'amount_paid': amount_paid,
            'remaining_to_pay': remaining_to_pay
        }
