from django.shortcuts import render,redirect,get_object_or_404
from .models import MedicalRecord,Visit,Laboratory,Patient
# Create your views here.
from .forms import PatientForm,MedicalRecordForm,VisitForm,LaboratoryForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PatientSerializer
from django.contrib.auth.decorators import login_required
from doctors.models import Doctor
from core.utils import is_reception,is_doctor
from patients.models import Patient
from django.http import HttpResponseForbidden
from appointments.models import Appointment

@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # redirect to dashboard after saving
    else:
        form = PatientForm()
    return render(request, 'patients/add_patient.html', {'form': form})

@login_required
def patient_list(request):
    if not is_reception(request.user):
        return HttpResponseForbidden("Not allowed")
    query = request.GET.get('q')
    if query:
        patients = Patient.objects.filter(name__icontains=query)
    else:
        patients = Patient.objects.all()
    return render(request,'patients/patient_list.html',{'patients':patients})


@login_required
def edit_patient(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'patients/add_patient.html', {'form': form})

@login_required    
def delete_patient(request,id):
    patient =Patient.objects.get(id=id)
    patient.delete()
    return redirect('patient_list')


@api_view(['GET'])
def api_patients(request):
    patients =Patient.objects.all()
    serializer =PatientSerializer(patients,many=True)
    return Response(serializer.data)
from billing.models import Bill
@login_required
def patient_detail(request,id):
    patient = get_object_or_404(Patient,id=id)
    records=MedicalRecord.objects.filter(patient=patient)
    labs=Laboratory.objects.filter(patient=patient)
    bills = Bill.objects.filter(
        patient=patient
    )
    return render(request,'patients/patient_detail.html',{
        'patient':patient,
        'records':records,
        'labs':labs,
        'bills':bills,
    })

@login_required
def add_medical_record(request,patient_id):
    if not is_doctor(request.user):
        return HttpResponseForbidden("Not allowed")
    patient = get_object_or_404(Patient,id=patient_id)

    if request.method =='POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            return redirect('patient_detail',id=patient.id)
    else:
        form = MedicalRecordForm()
        return render(request,'patients/add_medical_record.html',{
            'form':form,
            'patient':patient
        })
    

@login_required
def reception(request):
    visits = Visit.objects.all().order_by('-visit_date')

    return render(request, 'patients/reception.html', {
        'visits': visits
    })


@login_required
def add_visit(request):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reception')
    else:
        form = VisitForm()

    return render(request, 'patients/add_visit.html', {'form': form})

@login_required
def lab_list(request):
    labs = Laboratory.objects.all().order_by('-requested_date')
    return render(request,'patients/lab_list.html',{
        'labs':labs
    })

@login_required
def add_lab(request):
    if request.method =='POST':
        form = LaboratoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lab_list')
    else:
        form = LaboratoryForm()
    return render(request,'patients/add_lab.html',{'form':form})


@login_required
def patient_report(request,id):
    patient = get_object_or_404(Patient,id=id)
    records =MedicalRecord.objects.filter(patient=patient)
    labs = Laboratory.objects.filter(patient=patient)
    return render(request,'patients/patient_report.html',{
        'patient':patient,
        'records':records,
        'labs':labs
    })

@login_required
def doctor_dashboard(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return redirect('dashboard')
    visits = Visit.objects.filter(doctor=doctor)
    labs = Laboratory.objects.filter(doctor=doctor)
    records = MedicalRecord.objects.filter(doctor=doctor)
    return render(request,'patients/doctor_dashboard.html',{
        'visits':visits,
        'labs':labs,
        'records':records,
        'doctor':doctor
    })

@login_required
def reception_dashboard(request):
    if not is_reception(request.user):
        return HttpResponseForbidden("Not allowed")
    appointments = Appointment.objects.all()
    context = {
        'appointments':appointments
    }
    return render(request,'patients/reception_dashboard.html',context)
    visits = Visit.objects.all()

    return render(request,
                  'patients/reception_dashbaord.html',
                   {'visits':visits} 
                   )
