

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor
from .forms import DoctorForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DoctorSerializer
from django.contrib.auth.decorators import login_required
from core.utils import is_doctor
from django.http import HttpResponseForbidden
from patients.models import Patient,MedicalRecord,Visit


@login_required
def doctor_list(request):
    if not is_doctor(request.user):
        return HttpResponseForbidden("Not allowed")
    query = request.GET.get('q')
    if query:
        doctors = Doctor.objects.filter(name__icontains=query)
    else:
        doctors = Doctor.objects.all()
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})

@login_required
def add_doctor(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'doctors/add_doctor.html', {'form': form})

@login_required
def edit_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctors/add_doctor.html', {'form': form})

@login_required
def delete_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    doctor.delete()
    return redirect('doctor_list')

@api_view(['GET'])
def api_doctors(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)

@login_required
def doctor_dashboard(request):
    if not is_doctor(request.user):
        return HttpResponseForbidden("Not allowed")
    visits = Visit.objects.filter(doctor__user =request.user)
    return render(
        request,
        'doctors/doctor_dashboard.html',
        {'visits':visits}
    )
    
