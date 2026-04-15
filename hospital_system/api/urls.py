from django.urls import path
from patients.views import api_patients
from doctors.views import api_doctors
from appointments.views import api_appointments

urlpatterns = [
    path('patients/',api_patients),
    path('doctors/',api_doctors),
    path('appointments/',api_appointments),
]