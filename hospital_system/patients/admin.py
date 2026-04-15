from django.contrib import admin
from .models import Patient,MedicalRecord,Visit,Laboratory
# Register your models here.
admin.site.register(Patient)
admin.site.register(MedicalRecord)
admin.site.register(Visit)
admin.site.register(Laboratory)
