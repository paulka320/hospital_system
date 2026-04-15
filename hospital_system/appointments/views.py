

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment,Doctor
from .forms import AppointmentForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AppointmentSerializer
from django.contrib.auth.decorators import login_required


@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    doctor_id = request.GET.get('doctor')
    date = request.GET.get('date')
    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)

    if date:
        appointments = appointments.filter(date=date)
    doctors = Doctor.objects.all() 
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

@login_required
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/add_appointment_list.html', {'form': form})

@login_required
def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/add_appointment.html', {'form': form})

@login_required
def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.delete()
    return redirect('appointment_list')

@api_view(['GET'])
def api_appointments(request):
    appointments = Appointment.objects.all()
    serializer = AppointmentSerializer(appointments,many=True)
    return Response(serializer.data)