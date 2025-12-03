from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Season, Category, Member, Registration, Invoice

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
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
    parent = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    parent_email = serializers.EmailField(source='parent.email', read_only=True)
    parent_name = serializers.SerializerMethodField()

    def get_parent_name(self, obj):
        if obj.parent:
            return f"{obj.parent.first_name} {obj.parent.last_name}" if obj.parent.first_name else obj.parent.username
        return None

    class Meta:
        model = Member
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'birth_date', 'gender', 'address', 'license_number', 'has_passport', 'parent', 'parent_email', 'parent_name', 'weight_category']

class RegistrationSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)
    season = SeasonSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    member_id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), source='member', write_only=True)
    season_id = serializers.PrimaryKeyRelatedField(queryset=Season.objects.all(), source='season', write_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'member', 'season', 'category', 'status', 'paid', 'member_id', 'season_id', 'category_id', 'discount_percentage', 'discount_amount', 'payment_mode', 'installments_paid']

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
