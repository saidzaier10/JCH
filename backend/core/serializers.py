from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Season, Category, Member, Registration, Invoice, PaymentOption
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personnalisé pour l'obtention du token JWT.
    Ajoute des informations supplémentaires (is_staff, username) dans la réponse du token.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        data['is_staff'] = self.user.is_staff
        data['username'] = self.user.username
        return data

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'code', 'description', 'price', 'age_min', 'age_max']

class MemberSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Member.
    Inclut des champs calculés pour l'affichage (nom du parent, email du parent).
    """
    parent = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    parent_email = serializers.EmailField(source='parent.email', read_only=True)
    parent_name = serializers.SerializerMethodField()

    def get_parent_name(self, obj):
        if obj.parent:
            return f"{obj.parent.first_name} {obj.parent.last_name}" if obj.parent.first_name else obj.parent.username
        return None

    class Meta:
        model = Member
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'birth_date', 'gender', 'address', 'license_number', 'has_passport', 'parent', 'parent_email', 'parent_name', 'weight_category', 'discipline', 'belt', 'image_rights']

class PaymentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOption
        fields = ['id', 'name', 'installments', 'is_active']

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer pour les inscriptions.
    Gère la création (avec xxx_id) et la lecture (avec les objets imbriqués).
    Inclut les champs calculés pour les paiements (total à payer, payé, reste à payer).
    """
    member = MemberSerializer(read_only=True)
    season = SeasonSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    payment_option = PaymentOptionSerializer(read_only=True)
    
    # Champs en écriture seule pour la création/modification via ID
    member_id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), source='member', write_only=True)
    season_id = serializers.PrimaryKeyRelatedField(queryset=Season.objects.all(), source='season', write_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    payment_option_id = serializers.PrimaryKeyRelatedField(queryset=PaymentOption.objects.all(), source='payment_option', write_only=True, required=False, allow_null=True)

    # Champs calculés
    total_to_pay = serializers.SerializerMethodField()
    amount_paid = serializers.SerializerMethodField()
    remaining_to_pay = serializers.SerializerMethodField()

    class Meta:
        model = Registration
        fields = ['id', 'member', 'season', 'category', 'status', 'paid', 'member_id', 'season_id', 'category_id', 'discount_percentage', 'discount_amount', 'payment_mode', 'payment_option', 'payment_option_id', 'installments_paid', 'city_hall_aid', 'city_hall_aid_amount', 'has_supplementary_discipline', 'total_to_pay', 'amount_paid', 'remaining_to_pay']

    def get_payment_details(self, obj):
        if not hasattr(self, '_payment_details_cache'):
            self._payment_details_cache = {}
        if obj.id not in self._payment_details_cache:
            from .services import PriceCalculator
            self._payment_details_cache[obj.id] = PriceCalculator.get_payment_details(obj)
        return self._payment_details_cache[obj.id]

    def get_total_to_pay(self, obj):
        return self.get_payment_details(obj)['total_to_pay']

    def get_amount_paid(self, obj):
        return self.get_payment_details(obj)['amount_paid']

    def get_remaining_to_pay(self, obj):
        return self.get_payment_details(obj)['remaining_to_pay']

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
