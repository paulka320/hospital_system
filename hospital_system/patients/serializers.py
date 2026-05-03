from rest_framework import serializers
from .models import Patient, MedicalRecord, Visit, Laboratory, Prescription


class PatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'name', 'date_of_birth', 'age', 'gender', 'phone',
            'email', 'address', 'city', 'state', 'blood_type', 'emergency_contact',
            'emergency_contact_name', 'allergies', 'chronic_diseases',
            'insurance_provider', 'insurance_id', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'diagnosis', 'disease', 'prescription', 'visit_date',
            'review_date', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'visit_date']


class VisitSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = Visit
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'visit_date', 'status', 'notes', 'vitals', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'visit_date']


class LaboratorySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    test_type_display = serializers.CharField(source='get_test_type_display', read_only=True)
    
    class Meta:
        model = Laboratory
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'test_type', 'test_type_display', 'result', 'requested_date',
            'completed', 'completed_date', 'technician_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'requested_date']


class PrescriptionSerializer(serializers.ModelSerializer):
    medical_record_id = serializers.IntegerField(source='medical_record.id', read_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = Prescription
        fields = [
            'id', 'medical_record_id', 'patient', 'patient_name', 'doctor',
            'doctor_name', 'medicine_name', 'dosage', 'dosage_unit', 'frequency',
            'duration_days', 'instructions', 'status', 'created_at', 'filled_at', 'end_date'
        ]
        read_only_fields = ['id', 'created_at', 'filled_at']