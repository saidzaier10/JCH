"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from core.views import SeasonViewSet, CategoryViewSet, RegistrationViewSet, MemberViewSet, InvoiceViewSet, StatisticsView, UserRegistrationView, FamilyViewSet, HealthCheckView, CustomTokenObtainPairView, UserViewSet, PaymentOptionViewSet
from content.views import EventViewSet, GalleryImageViewSet
from communications.views import SendConvocationView, BulkEmailView
from attendance.views import CourseViewSet, SessionViewSet

router = DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'events', EventViewSet)
router.register(r'gallery', GalleryImageViewSet)
router.register(r'seasons', SeasonViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'registrations', RegistrationViewSet)
router.register(r'my-family', FamilyViewSet, basename='my-family')
router.register(r'courses', CourseViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'users', UserViewSet)
router.register(r'payment-options', PaymentOptionViewSet)

# Restrict admin to superusers
admin.site.has_permission = lambda r: r.user.is_active and r.user.is_superuser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('api/statistics/', StatisticsView.as_view(), name='statistics'),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/convocations/send/', SendConvocationView.as_view(), name='send_convocation'),
    path('api/emails/bulk-send/', BulkEmailView.as_view(), name='bulk_send_email'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/payments/', include('payments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
