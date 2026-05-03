from django.urls import path, include
from rest_framework.routers import DefaultRouter
from patients.api_views import PatientViewSet, MedicalRecordViewSet, VisitViewSet, LaboratoryViewSet, PrescriptionViewSet
from doctors.api_views import DoctorViewSet, DoctorAvailabilityViewSet, DoctorReviewViewSet
from appointments.api_views import AppointmentViewSet
from notifications.api_views import NotificationViewSet

# Create a router and register all viewsets
router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'medical-records', MedicalRecordViewSet, basename='medical-record')
router.register(r'visits', VisitViewSet, basename='visit')
router.register(r'laboratories', LaboratoryViewSet, basename='laboratory')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'doctor-availability', DoctorAvailabilityViewSet, basename='doctor-availability')
router.register(r'doctor-reviews', DoctorReviewViewSet, basename='doctor-review')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'notifications', NotificationViewSet, basename='notification')

# Include router URLs
urlpatterns = [
    path('', include(router.urls)),
]