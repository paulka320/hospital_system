from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, date, timedelta

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Appointment model.
    
    Endpoints:
    - GET /api/appointments/ - List all appointments
    - POST /api/appointments/ - Create new appointment
    - GET /api/appointments/{id}/ - Retrieve appointment detail
    - PUT /api/appointments/{id}/ - Update appointment
    - DELETE /api/appointments/{id}/ - Delete appointment
    - GET /api/appointments/upcoming/ - Get upcoming appointments
    - GET /api/appointments/today/ - Get today's appointments
    - POST /api/appointments/{id}/confirm/ - Confirm appointment
    - POST /api/appointments/{id}/cancel/ - Cancel appointment
    """
    
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Appointment.objects.all()
        
        # Filter by patient
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by doctor
        doctor_id = self.request.query_params.get('doctor_id')
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset.order_by('date', 'time')
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appointments"""
        now = timezone.now()
        appointments = Appointment.objects.filter(
            date__gte=now.date(),
            status__in=['scheduled', 'confirmed']
        ).order_by('date', 'time')
        
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's appointments"""
        today = timezone.now().date()
        appointments = Appointment.objects.filter(
            date=today,
            status__in=['scheduled', 'confirmed', 'in_progress']
        ).order_by('time')
        
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get past appointments"""
        today = timezone.now().date()
        appointments = Appointment.objects.filter(
            date__lt=today,
            status__in=['scheduled', 'confirmed']
        ).order_by('-date', '-time')
        
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm an appointment"""
        appointment = self.get_object()
        if appointment.status == 'scheduled':
            appointment.status = 'confirmed'
            appointment.save()
            
            # Send notification
            from notifications.services import create_notification
            create_notification(
                user=appointment.patient.user,
                notification_type='appointment_confirmed',
                title='Appointment Confirmed',
                message=f'Your appointment with Dr. {appointment.doctor.name} on {appointment.date} has been confirmed.',
                content_type='appointment',
                object_id=appointment.id
            )
            
            return Response(
                {'status': 'Appointment confirmed'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'Only scheduled appointments can be confirmed'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an appointment"""
        appointment = self.get_object()
        reason = request.data.get('reason', 'No reason provided')
        
        if appointment.status not in ['cancelled', 'completed']:
            appointment.status = 'cancelled'
            appointment.cancelled_reason = reason
            appointment.cancelled_at = timezone.now()
            appointment.save()
            
            # Send notification
            from notifications.services import create_notification
            create_notification(
                user=appointment.patient.user,
                notification_type='appointment_cancelled',
                title='Appointment Cancelled',
                message=f'Your appointment with Dr. {appointment.doctor.name} on {appointment.date} has been cancelled.',
                content_type='appointment',
                object_id=appointment.id
            )
            
            return Response(
                {'status': 'Appointment cancelled'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': 'This appointment cannot be cancelled'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark appointment as completed"""
        appointment = self.get_object()
        appointment.status = 'completed'
        appointment.save()
        
        return Response(
            {'status': 'Appointment marked as completed'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def reschedule(self, request, pk=None):
        """Reschedule an appointment"""
        appointment = self.get_object()
        new_date = request.data.get('date')
        new_time = request.data.get('time')
        
        if not new_date or not new_time:
            return Response(
                {'error': 'date and time are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment.date = new_date
        appointment.time = new_time
        appointment.status = 'rescheduled'
        appointment.save()
        
        return Response(
            {'status': 'Appointment rescheduled'},
            status=status.HTTP_200_OK
        )
