from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

from .models import Patient, MedicalRecord, Visit, Laboratory, Prescription
from .serializers import (
    PatientSerializer, MedicalRecordSerializer, VisitSerializer,
    LaboratorySerializer, PrescriptionSerializer
)


class PatientViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Patient model.
    
    Endpoints:
    - GET /api/patients/ - List all patients
    - POST /api/patients/ - Create new patient
    - GET /api/patients/{id}/ - Retrieve patient detail
    - PUT /api/patients/{id}/ - Update patient
    - DELETE /api/patients/{id}/ - Delete patient
    - GET /api/patients/{id}/medical-records/ - Get patient's medical records
    - GET /api/patients/{id}/visits/ - Get patient's visits
    - GET /api/patients/{id}/labs/ - Get patient's lab tests
    """
    
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Patient.objects.all()
        # Filter by name if provided
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        # Filter by blood type if provided
        blood_type = self.request.query_params.get('blood_type')
        if blood_type:
            queryset = queryset.filter(blood_type=blood_type)
        return queryset
    
    @action(detail=True, methods=['get'])
    def medical_records(self, request, pk=None):
        """Get all medical records for a patient"""
        patient = self.get_object()
        records = MedicalRecord.objects.filter(patient=patient)
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def visits(self, request, pk=None):
        """Get all visits for a patient"""
        patient = self.get_object()
        visits = Visit.objects.filter(patient=patient)
        serializer = VisitSerializer(visits, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def labs(self, request, pk=None):
        """Get all lab tests for a patient"""
        patient = self.get_object()
        labs = Laboratory.objects.filter(patient=patient)
        serializer = LaboratorySerializer(labs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def prescriptions(self, request, pk=None):
        """Get all prescriptions for a patient"""
        patient = self.get_object()
        prescriptions = Prescription.objects.filter(patient=patient)
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)


class MedicalRecordViewSet(viewsets.ModelViewSet):
    """API ViewSet for Medical Record model"""
    
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = MedicalRecord.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        doctor_id = self.request.query_params.get('doctor_id')
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        return queryset


class VisitViewSet(viewsets.ModelViewSet):
    """API ViewSet for Visit model"""
    
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Visit.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's visits"""
        from django.utils import timezone
        today = timezone.now().date()
        visits = Visit.objects.filter(visit_date=today)
        serializer = self.get_serializer(visits, many=True)
        return Response(serializer.data)


class LaboratoryViewSet(viewsets.ModelViewSet):
    """API ViewSet for Laboratory tests"""
    
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Laboratory.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        completed = self.request.query_params.get('completed')
        if completed is not None:
            queryset = queryset.filter(completed=completed.lower() == 'true')
        return queryset
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark a lab test as completed"""
        lab = self.get_object()
        from django.utils import timezone
        lab.completed = True
        lab.completed_date = timezone.now()
        lab.result = request.data.get('result', '')
        lab.technician_notes = request.data.get('technician_notes', '')
        lab.save()
        return Response(
            {'status': 'Lab test marked as completed'},
            status=status.HTTP_200_OK
        )


class PrescriptionViewSet(viewsets.ModelViewSet):
    """API ViewSet for Prescription model"""
    
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Prescription.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    @action(detail=True, methods=['post'])
    def mark_filled(self, request, pk=None):
        """Mark a prescription as filled"""
        prescription = self.get_object()
        from django.utils import timezone
        prescription.status = 'filled'
        prescription.filled_at = timezone.now()
        prescription.save()
        return Response(
            {'status': 'Prescription marked as filled'},
            status=status.HTTP_200_OK
        )
