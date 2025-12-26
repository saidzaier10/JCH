from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Event, GalleryImage
from .serializers import EventSerializer, GalleryImageSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

class GalleryImageViewSet(viewsets.ModelViewSet):
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    permission_classes = [AllowAny]

