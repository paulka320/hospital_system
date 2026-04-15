from django.urls import path
from . import views

urlpatterns = [
    path("",views.patient_list,name='patient_list'),
    path("add/",views.add_patient,name="add_patient"),
    path("edit/<int:id>/",views.edit_patient,name='edit_patient'),
    path("delete/<int:id>/",views.delete_patient,name='delete_patient'),
    path('detail/<int:id>/',views.patient_detail,name='patient_detail'),
    path('add-record/<int:patient_id>/',views.add_medical_record,name='add_medical_record'),
    path('reception/',views.reception,name='reception'),
    path('add-visit/',views.add_visit,name='add_visit'),
    path('laboratory/',views.lab_list,name='lab_list'),
    path('laboratory/add/',views.add_lab,name='add_lab'),
    path('report/<int:id>/',views.patient_report,name='patient_report'),
    path('doctor-dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    path('reception_dashboard/',views.reception_dashboard,name='reception_dashboard'),

]