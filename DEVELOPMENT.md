# Hospital Management System - Development Guide

## Architecture Overview

The HMS follows Django best practices with a modular architecture:

```
┌─────────────────────────────────────────┐
│         Frontend (Templates/HTML)       │
└────────────────────┬────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   ┌────▼─────┐           ┌──────▼──────┐
   │  Views   │           │  API Views   │
   │(Django)  │           │  (DRF)      │
   └────┬─────┘           └──────┬──────┘
        │                        │
        │    ┌──────────────────┬┴─────────┐
        │    │                  │          │
    ┌───▼────▼─┐      ┌────────▼──┐   ┌──▼────┐
    │ Forms    │      │Serializers│   │ Auth  │
    └──────────┘      └───────────┘   └───────┘
        │
    ┌───▼──────────────────────────────────┐
    │         Django ORM / Models           │
    │  ┌─────┬────────┬──────┬────────┐   │
    │  │Patients│Doctors│Appointments│Bills  │  │
    │  └─────┴────────┴──────┴────────┘   │
    └───┬──────────────────────────────────┘
        │
    ┌───▼──────────────────┐
    │   Database (SQLite)  │
    └──────────────────────┘
```

## Models Overview

### 1. Patient Model
Core patient information with medical history

**Fields:**
- Basic: name, date_of_birth, age, gender, phone, email
- Address: address, city, state
- Medical: blood_type, allergies, chronic_diseases
- Insurance: insurance_provider, insurance_id
- Contact: emergency_contact, emergency_contact_name
- Metadata: is_active, created_at, updated_at

**Relationships:**
- OneToOne → User (authentication)
- Reverse: medical_records, visits, laboratory_tests, prescriptions, appointments, bills

### 2. Doctor Model
Doctor profile and credentials

**Fields:**
- Basic: name, specialization, phone, email, gender
- Professional: qualification, experience_years, license_number
- Additional: bio, profile_picture, consultation_fee
- Status: is_available, average_rating, total_patients

**Relationships:**
- OneToOne → User (authentication)
- Reverse: availability, reviews, medical_records, visits, laboratory_tests, appointments, prescriptions

### 3. DoctorAvailability Model
Doctor working hours schedule

**Fields:**
- doctor (FK)
- day_of_week (0-6: Monday-Sunday)
- start_time, end_time
- is_available (Boolean)

**Unique Constraint:** (doctor, day_of_week)

### 4. DoctorReview Model
Patient reviews and ratings

**Fields:**
- doctor (FK)
- patient (FK, nullable)
- rating (1-5)
- comment (text)
- created_at

### 5. Appointment Model
Appointment scheduling

**Status Options:**
- scheduled, confirmed, in_progress, completed, cancelled, no_show, rescheduled

**Types:**
- consultation, follow_up, surgery, emergency, routine_check

**Fields:**
- patient, doctor, date, time
- appointment_type, status
- reason, notes
- cancelled_reason, cancelled_at
- created_at, updated_at

### 6. Visit Model
Patient visit tracking

**Status Options:**
- scheduled, waiting, in_progress, completed, cancelled

**Fields:**
- patient, doctor
- visit_date
- status, notes, vitals

### 7. MedicalRecord Model
Patient medical history

**Fields:**
- patient, doctor
- diagnosis, disease
- prescription (text)
- visit_date, review_date
- notes, created_at, updated_at

### 8. Laboratory Model
Lab test management

**Test Types:**
- blood, malaria, covid, urine, xray, ultrasound, ct_scan, ecg

**Fields:**
- patient, doctor, visit
- test_type
- result, requested_date
- completed, completed_date
- technician_notes

### 9. Prescription Model
Digital prescription management

**Dosage Units:**
- mg, ml, tablet, capsule, injection

**Status:**
- active, completed, cancelled, filled

**Fields:**
- medical_record, patient, doctor
- medicine_name, dosage, dosage_unit
- frequency, duration_days
- instructions, created_at, filled_at

### 10. Bill Model
Invoice and payment tracking

**Status:**
- draft, issued, paid, overdue, cancelled

**Payment Methods:**
- cash, card, check, online, insurance

**Fields:**
- bill_number, patient
- status, created_at, issued_at, due_date, paid_at
- subtotal, tax, discount, total_amount
- paid_amount, payment_method
- notes

### 11. BillItem Model
Line items in bills

**Item Types:**
- consultation, procedure, medicine, lab_test, room_charge, other

**Fields:**
- bill, description
- quantity, unit_price
- item_type, notes

### 12. Payment Model
Payment tracking

**Status:**
- pending, successful, failed, refunded

**Fields:**
- bill, amount, payment_method
- status, transaction_id
- notes, created_at, processed_at

### 13. Notification Model
User notifications

**Types:**
- appointment_reminder, appointment_confirmed, appointment_cancelled
- lab_result_ready, prescription_filled
- bill_issued, payment_received, general

**Fields:**
- user, notification_type
- title, message
- is_read, read_at
- content_type, object_id

## API Design Patterns

### ViewSet Structure
```python
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter based on query parameters
        pass
    
    @action(detail=False, methods=['get'])
    def custom_action(self, request):
        # Custom endpoint
        pass
```

### Common Query Parameters
```
?name=<search>          # Search by name
?doctor_id=<id>         # Filter by doctor
?patient_id=<id>        # Filter by patient
?status=<status>        # Filter by status
?start_date=<date>      # Filter by start date
?end_date=<date>        # Filter by end date
```

## Form Classes

### PatientForm
```python
- name, date_of_birth, age, gender, phone
- email, address, city, state
- blood_type, emergency_contact
- allergies, chronic_diseases
- insurance details
```

### DoctorForm
```python
- name, specialization, phone, email
- gender, qualification, experience_years
- license_number, bio, profile_picture
- consultation_fee
```

### AppointmentForm
```python
- patient, doctor, date, time
- appointment_type, reason, notes
```

## Views Structure

### Web Views (Traditional Django Views)
- patient_list, add_patient, edit_patient, delete_patient
- patient_detail, patient_report
- doctor_list, add_doctor, edit_doctor, delete_doctor
- doctor_dashboard
- add_medical_record, add_visit, add_lab
- reception, lab_list

### API Views (Django REST Framework ViewSets)
- PatientViewSet with custom actions
- DoctorViewSet with search and availability
- AppointmentViewSet with scheduling actions
- MedicalRecordViewSet with filtering
- And more...

## Utility Functions

### Authentication Helpers (core/utils.py)
```python
is_reception(user)      # Check if user is reception
is_doctor(user)         # Check if user is doctor
is_admin(user)          # Check if user is admin
```

### Notification Services (notifications/services.py)
```python
create_notification()           # Create notification
send_appointment_reminder()     # Send reminder
send_lab_result_ready()         # Send lab result
send_bill_issued()              # Send bill notification
```

## Database Queries

### Optimized Queries

**Get patient with all related data:**
```python
from django.db.models import Prefetch

patient = Patient.objects.prefetch_related(
    'medical_records',
    'visits',
    'laboratory_tests',
    'prescriptions'
).get(id=1)
```

**Get doctor appointments for date:**
```python
from datetime import date
appointments = Appointment.objects.filter(
    doctor_id=1,
    date=date.today(),
    status__in=['scheduled', 'confirmed']
).order_by('time')
```

**Get patient lab results:**
```python
lab_results = Laboratory.objects.filter(
    patient_id=1,
    completed=True
).order_by('-completed_date')
```

## Testing Strategy

### Unit Tests
```python
# tests/test_models.py
class PatientModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(...)
    
    def test_patient_creation(self):
        self.assertTrue(isinstance(self.patient, Patient))
```

### API Tests
```python
# tests/test_api.py
class PatientAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(...)
        self.client.force_authenticate(user=self.user)
    
    def test_list_patients(self):
        response = self.client.get('/api/patients/')
        self.assertEqual(response.status_code, 200)
```

## Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Update ALLOWED_HOSTS
- [ ] Use environment variables for sensitive data
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up static files serving
- [ ] Configure logging
- [ ] Enable HTTPS
- [ ] Set up CORS if needed
- [ ] Configure email backend
- [ ] Run collectstatic
- [ ] Run database migrations
- [ ] Create superuser
- [ ] Set up monitoring and logging

## Performance Tips

1. **Database Optimization**
   - Use select_related for ForeignKey
   - Use prefetch_related for reverse relations
   - Add database indexes on frequently filtered fields
   - Use pagination for large result sets

2. **Caching**
   - Cache doctor availability
   - Cache frequently accessed patient data
   - Use Redis for session store

3. **API Optimization**
   - Implement pagination
   - Use filtering to reduce results
   - Consider field limiting
   - Use compression (gzip)

## Common Issues & Solutions

### Issue: Appointment conflicts
**Solution:** Add unique_together constraint or check availability in view

### Issue: Circular imports
**Solution:** Import models locally or use string references ('app.Model')

### Issue: N+1 queries
**Solution:** Use select_related() and prefetch_related()

## Code Style Guidelines

- Follow PEP 8
- Use meaningful variable names
- Document complex logic
- Add docstrings to functions
- Keep views simple (logic in models)
- Use managers for complex queries

## Useful Django Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Shell
python manage.py shell

# Admin user management
python manage.py createsuperuser
python manage.py changepassword <username>

# Dump data
python manage.py dumpdata > backup.json

# Load data
python manage.py loaddata backup.json

# Collect static files
python manage.py collectstatic

# Clear cache
python manage.py clear_cache
```

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Models](https://docs.djangoproject.com/en/6.0/topics/db/models/)
- [Django Admin](https://docs.djangoproject.com/en/6.0/ref/contrib/admin/)
