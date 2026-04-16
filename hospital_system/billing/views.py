from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseForbidden
from core.utils import is_reception
from .models import Bill


def billing_dashboard(request):

    if not is_reception(request.user):
        return HttpResponseForbidden("Not allowed")

    bills = Bill.objects.all().order_by('-created_at')

    return render(
        request,
        'billing/billing_dashboard.html',
        {'bills': bills}
    )


from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from core.utils import is_reception
from .models import Bill
from patients.models import Patient


def create_bill(request):

    if not is_reception(request.user):
        return HttpResponseForbidden("Not allowed")

    patients = Patient.objects.all()

    if request.method == "POST":

        patient_id = request.POST.get('patient')

        patient = Patient.objects.get(id=patient_id)

        Bill.objects.create(
            patient=patient
        )

        return redirect('billing_dashboard')

    return render(
        request,
        'billing/create_bill.html',
        {'patients': patients}
    )