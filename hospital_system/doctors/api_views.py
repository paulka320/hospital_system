from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Doctor, DoctorAvailability, DoctorReview
from .serializers import DoctorSerializer, DoctorAvailabilitySerializer, DoctorReviewSerializer, DoctorDetailSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Doctor model.
    
    Endpoints:
    - GET /api/doctors/ - List all doctors
    - POST /api/doctors/ - Create new doctor
    - GET /api/doctors/{id}/ - Retrieve doctor detail
    - GET /api/doctors/search/ - Search doctors by specialization
    - GET /api/doctors/{id}/availability/ - Get doctor's availability
    - GET /api/doctors/{id}/reviews/ - Get doctor's reviews
    """
    
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DoctorDetailSerializer
        return DoctorSerializer
    
    def get_queryset(self):
        queryset = Doctor.objects.all()
        # Filter by specialization
        specialization = self.request.query_params.get('specialization')
        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)
        # Filter by availability
        is_available = self.request.query_params.get('is_available')
        if is_available is not None:
            queryset = queryset.filter(is_available=is_available.lower() == 'true')
        return queryset
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search doctors by name or specialization"""
        query = request.query_params.get('q', '')
        if query:
            doctors = Doctor.objects.filter(
                name__icontains=query
            ) | Doctor.objects.filter(
                specialization__icontains=query
            )
        else:
            doctors = Doctor.objects.all()
        
        serializer = self.get_serializer(doctors, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get doctor's availability schedule"""
        doctor = self.get_object()
        availability = DoctorAvailability.objects.filter(doctor=doctor)
        serializer = DoctorAvailabilitySerializer(availability, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get doctor's reviews and ratings"""
        doctor = self.get_object()
        reviews = DoctorReview.objects.filter(doctor=doctor)
        serializer = DoctorReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        """Get doctor's appointments"""
        from appointments.models import Appointment
        from appointments.serializers import AppointmentSerializer
        
        doctor = self.get_object()
        status_filter = request.query_params.get('status')
        
        appointments = Appointment.objects.filter(doctor=doctor)
        if status_filter:
            appointments = appointments.filter(status=status_filter)
        
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    """API ViewSet for Doctor Availability"""
    
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = DoctorAvailability.objects.all()
        doctor_id = self.request.query_params.get('doctor_id')
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        return queryset


class DoctorReviewViewSet(viewsets.ModelViewSet):
    """API ViewSet for Doctor Reviews"""
    
    queryset = DoctorReview.objects.all()
    serializer_class = DoctorReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = DoctorReview.objects.all()
        doctor_id = self.request.query_params.get('doctor_id')
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        return queryset
    
    def perform_create(self, serializer):
        # Set the patient from the authenticated user if available
        serializer.save()
