from django import forms
from .models import Patient,MedicalRecord,Visit,Laboratory

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'phone', 'gender', 'age']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['doctor','diagnosis','disease','prescription','review_date']
        widgets ={
            'doctor':forms.Select(attrs={'class':'form-select'}),
            'diagnosis':forms.Textarea(attrs={'class':'form-control'}),
            'disease':forms.TextInput(attrs={'class':'form-control'}),
            'prescription':forms.Textarea(attrs={'class':'form-control'}),
            'review_date':forms.DateInput(attrs={'type':'date','class':'form-control'}),
        }


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['patient', 'doctor']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
        }

class LaboratoryForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields =['patient','doctor','visit','test_type','result','completed']
        widgets = {
            'patient':forms.Select(attrs={'class':'form-select'}),
            'doctor':forms.Select(attrs={'class':'form-select'}),
            'visit':forms.Select(attrs={'class':'form-select'}),
            'test_type':forms.Select(attrs={'class':'form-select'}),
            'result':forms.Textarea(attrs={'class':'form-control'}),
        }