from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum
from .models import Season, Category, Member, Registration, Invoice, PaymentOption
from content.models import Convocation
from .serializers import (
    SeasonSerializer, CategorySerializer, MemberSerializer, 
    RegistrationSerializer, InvoiceSerializer, CustomTokenObtainPairSerializer, UserSerializer,
    PaymentOptionSerializer
)
from django.db import connection
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class HealthCheckView(views.APIView):
    """
    Vue de vérification de l'état de santé de l'application (Health Check).
    Utilisée par Docker/Kubernetes pour vérifier si le service est en ligne et si la base de données est accessible.
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
    Vue API pour récupérer les indicateurs clés de performance (KPI) et statistiques du club.
    Retourne les données pour:
    - Répartition par catégorie
    - Répartition par genre
    - Revenus totaux
    - Nombre total d'adhérents
    """
    def get(self, request):
        # Saison active
        active_season = Season.objects.filter(is_active=True).first()
        if not active_season:
            # Return empty structure instead of 404 to avoid frontend global error toast
            return Response({
                'season': 'Aucune saison active',
                'registrations_per_category': [],
                'gender_distribution': [],
                'total_revenue': 0,
                'total_members': 0
            })

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

from .serializers import (
    SeasonSerializer, CategorySerializer, MemberSerializer, 
    RegistrationSerializer, InvoiceSerializer, CustomTokenObtainPairSerializer, UserSerializer,
    PaymentOptionSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des utilisateurs (réservé aux administrateurs).
    En lecture seule (READ-ONLY) partiel pour ne pas interférer avec le processus d'inscription spécifique.
    Permet aux admins de lister et rechercher des utilisateurs.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['username', 'email']
    search_fields = ['username', 'email', 'first_name', 'last_name']

class UserRegistrationView(views.APIView):
    """
    Vue dédiée à l'inscription des nouveaux parents (création de compte utilisateur).
    Accessible publiquement (AllowAny).
    Gère la création du User Django et génère les tokens JWT initiaux.
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
    ViewSet pour gérer les saisons sportives.
    Permet de créer, modifier, lister et activer une saison.
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
        """
        Endpoint personnalisé pour récupérer la saison actuellement active.
        """
        active_season = Season.objects.filter(is_active=True).first()
        if active_season:
            serializer = self.get_serializer(active_season)
            return Response(serializer.data)
        return Response({'detail': 'Aucune saison active trouvée'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Action pour définir une saison comme "active".
        Cela désactivera automatiquement toutes les autres saisons (logique dans le modèle ou via signal, 
        ici simple bascule champ is_active).
        """
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

class PaymentOptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les options de paiement.
    """
    queryset = PaymentOption.objects.all()
    serializer_class = PaymentOptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Or Admin only for writes


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
    ViewSet pour la gestion des fiches adhérents (enfants/membres).
    - Les administrateurs voient tous les membres.
    - Les parents connectés ne voient que les membres rattachés à leur compte (leurs enfants).
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
        # Admin can set 'parent' explicitly via serializer
        if self.request.user.is_staff:
            parent = serializer.validated_data.get('parent')
            if parent:
                 serializer.save(parent=parent)
            else:
                 # Si l'admin crée un membre sans spécifier de parent, 
                 # on l'assigne par défaut à l'admin lui-même (ou on laisse None selon le besoin).
                 # Ici, on assigne à l'utilisateur courant (l'admin) pour éviter les orphelins.
                 serializer.save(parent=self.request.user)
        # Regular user always assigns to themselves
        elif self.request.user.is_authenticated:
            serializer.save(parent=self.request.user)
        else:
            # Should not happen due to permissions, but safe fallback
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
    ViewSet "Tableau de bord famille".
    Regroupe toutes les informations pertinentes pour une famille connecté :
    - Liste des enfants inscrits
    - Inscriptions actives
    - Convocations aux compétitions
    - Factures
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        members = Member.objects.filter(parent=user)
        
        # Serialize members
        members_data = MemberSerializer(members, many=True).data

        # Add active registration info to each member
        active_season = Season.objects.filter(is_active=True).first()
        if active_season:
            for member_data in members_data:
                member_id = member_data['id']
                registration = Registration.objects.filter(member_id=member_id, season=active_season).first()
                if registration:
                    # Use serializer to get computed fields (total_to_pay, etc.)
                    reg_data = RegistrationSerializer(registration).data
                    member_data['active_registration'] = reg_data
                else:
                    member_data['active_registration'] = None

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

