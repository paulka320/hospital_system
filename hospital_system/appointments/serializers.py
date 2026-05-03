from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    is_upcoming = serializers.SerializerMethodField()
    is_today = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name', 
            'doctor_specialization', 'date', 'time', 'appointment_type', 'status',
            'reason', 'notes', 'is_upcoming', 'is_today', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_is_upcoming(self, obj):
        return obj.is_upcoming()
    
    def get_is_today(self, obj):
        return obj.is_today()