from rest_framework import serializers
from .models import Course, Session, Attendance
from core.serializers import MemberSerializer

class CourseSerializer(serializers.ModelSerializer):
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    member_details = MemberSerializer(source='member', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'session', 'member', 'member_details', 'status']

class SessionSerializer(serializers.ModelSerializer):
    attendances = AttendanceSerializer(many=True, read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'course', 'course_name', 'date', 'notes', 'attendances']
