from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum
from .models import Season, Category, Member, Registration, Invoice
from content.models import Convocation
from .serializers import (
    SeasonSerializer, CategorySerializer, MemberSerializer, 
    RegistrationSerializer, InvoiceSerializer, CustomTokenObtainPairSerializer
)
from django.db import connection
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class HealthCheckView(views.APIView):
    """
    Endpoint de vérification de santé pour Docker/K8s.
    Vérifie la connexion DB.
    """
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return Response({'status': 'ok', 'database': 'connected'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'database': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class StatisticsView(views.APIView):
    """
    Vue pour récupérer les statistiques du club (KPIs, graphiques).
    """
    def get(self, request):
        # Saison active
        active_season = Season.objects.filter(is_active=True).first()
        if not active_season:
            return Response({'error': 'Aucune saison active'}, status=404)

        # 1. Inscriptions par catégorie
        registrations_per_category = Registration.objects.filter(season=active_season) \
            .values('category__name') \
            .annotate(count=Count('id')) \
            .order_by('-count')

        # 2. Répartition par genre
        gender_distribution = Member.objects.filter(registrations__season=active_season) \
            .values('gender') \
            .annotate(count=Count('id'))

        # 3. Revenu total (Inscriptions payées * Prix de la catégorie)
        total_revenue = 0
        paid_registrations = Registration.objects.filter(season=active_season, paid=True)
        for reg in paid_registrations:
            total_revenue += reg.category.price

        # 4. Nombre total d'adhérents
        total_members = Registration.objects.filter(season=active_season).count()

        data = {
            'season': active_season.name,
            'registrations_per_category': list(registrations_per_category),
            'gender_distribution': list(gender_distribution),
            'total_revenue': total_revenue,
            'total_members': total_members
        }
        return Response(data)

from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import permissions

class UserRegistrationView(views.APIView):
    """
    Vue pour l'inscription des parents (création de compte utilisateur).
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password:
            return Response({'error': 'Nom d\'utilisateur et mot de passe requis'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Ce nom d\'utilisateur existe déjà'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Generate tokens
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'id': user.id, 
            'username': user.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)

class SeasonViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les saisons.
    """
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'activate']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retourne la saison active."""
        active_season = Season.objects.filter(is_active=True).first()
        if active_season:
            serializer = self.get_serializer(active_season)
            return Response(serializer.data)
        return Response({'detail': 'Aucune saison active trouvée'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Active une saison et désactive les autres."""
        season = self.get_object()
        season.is_active = True
        season.save()
        return Response({'status': 'Saison activée', 'season': season.name})

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour visualiser les catégories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class RegistrationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les inscriptions.
    """
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def export(self, request):
        """
        Exporte les inscriptions en Excel.
        """
        from .utils import export_registrations_to_excel
        queryset = self.filter_queryset(self.get_queryset())
        return export_registrations_to_excel(queryset)

    @action(detail=True, methods=['get'])
    def price_details(self, request, pk=None):
        """
        Retourne les détails du calcul du prix pour cette inscription.
        """
        from .services import PriceCalculator
        registration = self.get_object()
        details = PriceCalculator.calculate_price(registration)
        return Response(details)

class MemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les adhérents.
    Les utilisateurs connectés ne voient que leurs enfants.
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Member.objects.all()
        if user.is_authenticated:
            return Member.objects.filter(parent=user)
        return Member.objects.none()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(parent=self.request.user)
        else:
            serializer.save()

class InvoiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les factures.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Génère et télécharge le PDF de la facture.
        """
        from django.http import HttpResponse
        from .pdf_generator import generate_invoice_pdf
        
        invoice = self.get_object()
        pdf = generate_invoice_pdf(invoice)
        
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"Facture_{invoice.id}_{invoice.member.last_name}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        return Response({'error': 'Erreur lors de la génération du PDF'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FamilyViewSet(viewsets.ViewSet):
    """
    ViewSet pour récupérer les données de la famille connectée (Enfants, Convocations, Factures).
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        members = Member.objects.filter(parent=user)
        
        # Serialize members
        members_data = MemberSerializer(members, many=True).data
        
        # Get convocations for these members
        convocations = Convocation.objects.filter(member__in=members).order_by('-event__start_time')
        # We need a serializer for convocations, or build it manually for now
        convocations_data = []
        for conv in convocations:
            convocations_data.append({
                'id': conv.id,
                'event_title': conv.event.title,
                'event_date': conv.event.start_time,
                'event_location': conv.event.location,
                'member_name': f"{conv.member.first_name}",
                'status': conv.get_status_display(),
                'status_code': conv.status
            })

        # Get invoices for these members
        invoices = Invoice.objects.filter(member__in=members).order_by('-date_issued')
        invoices_data = InvoiceSerializer(invoices, many=True).data

        return Response({
            'children': members_data,
            'convocations': convocations_data,
            'invoices': invoices_data
        })

