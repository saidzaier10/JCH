from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course, Session, Attendance
from .serializers import CourseSerializer, SessionSerializer, AttendanceSerializer
from core.models import Member

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e), 'traceback': traceback.format_exc()}, status=status.HTTP_400_BAD_REQUEST)

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    @action(detail=False, methods=['get'])
    def get_by_date_and_course(self, request):
        date = request.query_params.get('date')
        course_id = request.query_params.get('course_id')

        if not date or not course_id:
            return Response({'error': 'Date and course_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        session, created = Session.objects.get_or_create(date=date, course_id=course_id)
        serializer = self.get_serializer(session)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_attendance(self, request, pk=None):
        session = self.get_object()
        attendances_data = request.data.get('attendances', [])

        for item in attendances_data:
            member_id = item.get('member_id')
            status_val = item.get('status')
            
            Attendance.objects.update_or_create(
                session=session,
                member_id=member_id,
                defaults={'status': status_val}
            )

        return Response({'status': 'success'})
