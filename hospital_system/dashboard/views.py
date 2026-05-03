from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from billing.models import Bill
from core.utils import is_reception, is_lab


@login_required
def dashboard(request):
    """
    Main dashboard view with role-based redirection
    """
    # Check user role and redirect to appropriate dashboard
    if request.user.profile.is_doctor:
        return redirect('doctor_dashboard')
    elif request.user.profile.is_receptionist:
        return redirect('reception_dashboard')
    elif request.user.profile.is_lab_technician:
        return redirect('lab_dashboard')

    # Default dashboard for admin/other roles
    context = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'pending_tasks': Appointment.objects.filter(status='scheduled').count(),
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def dashboard_view(request):
    """Legacy dashboard view - redirects to main dashboard"""
    return redirect('dashboard')


@login_required
def doctor_dashboard(request):
    """
    Doctor-specific dashboard showing their appointments and patients
    """
    if not request.user.profile.is_doctor:
        return redirect('dashboard')

    try:
        doctor = Doctor.objects.get(user=request.user)
        appointments = Appointment.objects.filter(doctor=doctor)
        
        context = {
            'doctor': doctor,
            'total_appointments': appointments.count(),
            'upcoming_appointments': appointments.filter(status__in=['scheduled', 'confirmed']).count(),
            'completed_appointments': appointments.filter(status='completed').count(),
            'total_patients': Patient.objects.filter(appointment__doctor=doctor).distinct().count(),
        }
    except Doctor.DoesNotExist:
        context = {
            'error': 'Doctor profile not found'
        }
    
    return render(request, 'dashboard/doctor_dashboard.html', context)


@login_required
def reception_dashboard(request):
    """
    Reception-specific dashboard for appointment management and patient check-ins
    """
    if not request.user.profile.is_receptionist:
        return redirect('dashboard')

    context = {
        'total_patients': Patient.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'today_appointments': Appointment.objects.filter(date=None).count(),
        'pending_check_ins': Appointment.objects.filter(status='scheduled').count(),
    }
    return render(request, 'dashboard/reception_dashboard.html', context)


@login_required
def lab_dashboard(request):
    """
    Laboratory technician dashboard
    """
    if not request.user.profile.is_lab_technician:
        return redirect('dashboard')

    from patients.models import Laboratory
    
    context = {
        'total_tests': Laboratory.objects.count(),
        'pending_tests': Laboratory.objects.filter(status='pending').count(),
        'completed_tests': Laboratory.objects.filter(status='completed').count(),
    }
    return render(request, 'dashboard/lab_dashboard.html', context)
    