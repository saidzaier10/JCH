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
            
        # Family Discount
        family_discount_amount = category_price * discount_percentage
        price_after_family_discount = category_price - family_discount_amount
        
        # Manual Discounts
        manual_discount_percent = registration.discount_percentage / 100
        manual_discount_amount_from_percent = price_after_family_discount * manual_discount_percent
        
        final_price = price_after_family_discount - manual_discount_amount_from_percent - registration.discount_amount
        
        # Ensure price doesn't go below 0
        if final_price < 0:
            final_price = Decimal('0.00')
        
        return {
            'base_price': category_price,
            'family_discount_percentage': discount_percentage * 100,
            'family_discount_amount': family_discount_amount,
            'manual_discount_percentage': registration.discount_percentage,
            'manual_discount_amount': registration.discount_amount,
            'final_price': final_price,
            'rank': rank
        }
