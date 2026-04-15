from django.shortcuts import render,redirect
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from django.contrib.auth.decorators import login_required
from core.utils import is_reception,is_lab

# Create your views here.
@login_required
def dashboard_view(request):
    context= {
        'doctors':Doctor.objects.count(),
        'patients':Patient.objects.count(),
        'appointments':Appointment.objects.count()
    }
    return render(request,'dashboard/dashboard.html',context)

@login_required
def dashboard(request):
    if Doctor.objects.filter(user=request.user).exists():
        return redirect('doctor_dashboard')
    elif is_reception(request.user):
        return redirect('reception_dashboard')
    elif is_lab(request.user):
        return redirect('lab_dashboard')

    
    total_patients= Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()

    
    return render(request,'dashboard/dashboard.html',{
        'total_patients':total_patients,
        'total_doctors':total_doctors,
        'total_appointments':total_appointments,
    })
    