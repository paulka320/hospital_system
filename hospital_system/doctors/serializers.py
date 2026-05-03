from rest_framework import serializers
from .models import Doctor, DoctorAvailability, DoctorReview


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = DoctorAvailability
        fields = ['id', 'doctor', 'day_of_week', 'day_of_week_display', 'start_time', 'end_time', 'is_available']


class DoctorReviewSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    
    class Meta:
        model = DoctorReview
        fields = ['id', 'doctor', 'patient', 'patient_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']


class DoctorSerializer(serializers.ModelSerializer):
    availability = DoctorAvailabilitySerializer(many=True, read_only=True)
    reviews = DoctorReviewSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    total_patients = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'name', 'specialization', 'phone', 'email', 'gender',
            'qualification', 'experience_years', 'license_number', 'bio',
            'profile_picture', 'is_available', 'consultation_fee', 'total_patients',
            'average_rating', 'availability', 'reviews', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'average_rating', 'total_patients']


class DoctorDetailSerializer(DoctorSerializer):
    """Extended doctor serializer with appointment information"""
    appointment_count = serializers.SerializerMethodField()
    
    def get_appointment_count(self, obj):
        from appointments.models import Appointment
        return Appointment.objects.filter(doctor=obj, status__in=['scheduled', 'confirmed']).count()