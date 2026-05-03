# API Testing Guide

## Getting Started

### Prerequisites
- Install curl or Postman for API testing
- Have the development server running: `python manage.py runserver`
- Get an authentication token (see Authentication section)

## Authentication

### Get Token
```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

Response:
```json
{
  "token": "abc123xyz..."
}
```

### Using Token in Requests
```bash
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/patients/
```

## Patient API Tests

### List All Patients
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/patients/
```

### Search Patients by Name
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/patients/?name=John"
```

### Filter by Blood Type
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/patients/?blood_type=O%2B"
```

### Create Patient
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "date_of_birth": "1990-05-15",
    "age": 34,
    "gender": "M",
    "phone": "+234800000000",
    "email": "john@example.com",
    "blood_type": "O+",
    "address": "123 Main Street",
    "city": "Lagos",
    "state": "Lagos"
  }'
```

### Get Patient Detail
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/patients/1/
```

### Get Patient Medical Records
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/patients/1/medical-records/
```

### Get Patient Visits
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/patients/1/visits/
```

### Get Patient Labs
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/patients/1/labs/
```

### Get Patient Prescriptions
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/patients/1/prescriptions/
```

### Update Patient
```bash
curl -X PUT http://localhost:8000/api/patients/1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+234900000000",
    "email": "newemail@example.com"
  }'
```

### Delete Patient
```bash
curl -X DELETE http://localhost:8000/api/patients/1/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## Doctor API Tests

### List All Doctors
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/doctors/
```

### Search Doctors
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/doctors/search/?q=Cardiologist"
```

### Filter by Specialization
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/doctors/?specialization=Cardiology"
```

### Get Available Doctors
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/doctors/?is_available=true"
```

### Create Doctor
```bash
curl -X POST http://localhost:8000/api/doctors/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Jane Smith",
    "specialization": "Cardiology",
    "phone": "+234810000000",
    "email": "jane@hospital.com",
    "gender": "F",
    "qualification": "MD, Cardiology",
    "experience_years": 10,
    "license_number": "LN12345",
    "consultation_fee": "5000.00"
  }'
```

### Get Doctor Detail
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/doctors/1/
```

### Get Doctor Availability
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/doctors/1/availability/
```

### Get Doctor Reviews
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/doctors/1/reviews/
```

### Get Doctor Appointments
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/doctors/1/appointments/
```

## Appointment API Tests

### List All Appointments
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/appointments/
```

### Get Upcoming Appointments
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/appointments/upcoming/
```

### Get Today's Appointments
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/appointments/today/
```

### Filter by Status
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/appointments/?status=confirmed"
```

### Filter by Date Range
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/appointments/?start_date=2026-05-01&end_date=2026-05-31"
```

### Create Appointment
```bash
curl -X POST http://localhost:8000/api/appointments/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient": 1,
    "doctor": 1,
    "date": "2026-05-20",
    "time": "10:00:00",
    "appointment_type": "consultation",
    "reason": "General checkup"
  }'
```

### Confirm Appointment
```bash
curl -X POST http://localhost:8000/api/appointments/1/confirm/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Cancel Appointment
```bash
curl -X POST http://localhost:8000/api/appointments/1/cancel/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Patient request"
  }'
```

### Reschedule Appointment
```bash
curl -X POST http://localhost:8000/api/appointments/1/reschedule/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-05-25",
    "time": "14:00:00"
  }'
```

### Mark Appointment as Completed
```bash
curl -X POST http://localhost:8000/api/appointments/1/mark-completed/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## Medical Record API Tests

### List All Medical Records
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/medical-records/
```

### Filter by Patient
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/medical-records/?patient_id=1"
```

### Filter by Doctor
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/medical-records/?doctor_id=1"
```

### Create Medical Record
```bash
curl -X POST http://localhost:8000/api/medical-records/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient": 1,
    "doctor": 1,
    "diagnosis": "Hypertension",
    "disease": "High Blood Pressure",
    "prescription": "Atenolol 50mg daily",
    "notes": "Follow up in 2 weeks"
  }'
```

## Laboratory API Tests

### List All Lab Tests
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/laboratories/
```

### Filter by Patient
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/laboratories/?patient_id=1"
```

### Filter by Completion Status
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/laboratories/?completed=false"
```

### Create Lab Test
```bash
curl -X POST http://localhost:8000/api/laboratories/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient": 1,
    "doctor": 1,
    "test_type": "blood"
  }'
```

### Mark Lab Test as Completed
```bash
curl -X POST http://localhost:8000/api/laboratories/1/mark-completed/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "result": "Normal - All values within range",
    "technician_notes": "Blood sample collected successfully"
  }'
```

## Prescription API Tests

### List All Prescriptions
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/prescriptions/
```

### Filter by Patient
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/prescriptions/?patient_id=1"
```

### Filter by Status
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/prescriptions/?status=active"
```

### Create Prescription
```bash
curl -X POST http://localhost:8000/api/prescriptions/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "medical_record": 1,
    "patient": 1,
    "doctor": 1,
    "medicine_name": "Atenolol",
    "dosage": 50,
    "dosage_unit": "mg",
    "frequency": "Once daily",
    "duration_days": 30,
    "instructions": "Take in the morning with breakfast"
  }'
```

### Mark Prescription as Filled
```bash
curl -X POST http://localhost:8000/api/prescriptions/1/mark-filled/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## Notification API Tests

### Get User Notifications
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/notifications/
```

### Get Unread Notifications
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/notifications/unread/
```

### Mark Notification as Read
```bash
curl -X POST http://localhost:8000/api/notifications/1/mark-as-read/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Mark All Notifications as Read
```bash
curl -X POST http://localhost:8000/api/notifications/mark-all-read/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Get Notification Preferences
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/notifications/preferences/
```

### Update Notification Preferences
```bash
curl -X PUT http://localhost:8000/api/notifications/preferences/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email_notifications": true,
    "sms_notifications": false,
    "push_notifications": true,
    "appointment_reminders": true,
    "lab_results": true,
    "billing_alerts": true
  }'
```

### Delete All Notifications
```bash
curl -X DELETE http://localhost:8000/api/notifications/delete-all/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## Postman Collection Import

You can import these requests into Postman:

1. Create a new collection "Hospital Management System"
2. Add these requests with the appropriate authentication token
3. Set environment variables for:
   - `base_url`: http://localhost:8000
   - `token`: Your authentication token
   - `patient_id`: Default patient ID to test
   - `doctor_id`: Default doctor ID to test

## Common Response Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 204 | No Content - Successful deletion |
| 400 | Bad Request - Invalid data |
| 401 | Unauthorized - Missing authentication |
| 403 | Forbidden - Permission denied |
| 404 | Not Found - Resource not found |
| 500 | Server Error - Internal error |

## Error Handling

### Example Error Response
```json
{
  "error": "Field is required",
  "field": "diagnosis"
}
```

### Validation Error Response
```json
{
  "non_field_errors": [
    "The fields patient, doctor, date, time must make a unique set."
  ]
}
```

## Performance Testing

### Pagination
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/patients/?page=2"
```

### Filtering with Multiple Parameters
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/appointments/?doctor_id=1&status=confirmed&start_date=2026-05-01"
```

## Tips for Testing

1. **Use environment variables** in Postman to manage tokens and base URLs
2. **Test error cases** - invalid data, missing fields, unauthorized access
3. **Verify pagination** with large datasets
4. **Check filtering** with various parameter combinations
5. **Test relationships** - nested data in responses
6. **Validate status codes** for each operation type
7. **Check timestamps** - created_at, updated_at fields

## Debugging

### Enable Django Debug Toolbar
Add to INSTALLED_APPS in settings.py:
```python
'debug_toolbar',
```

### Add to MIDDLEWARE:
```python
'debug_toolbar.middleware.DebugToolbarMiddleware',
```

### Check API Logs
```bash
tail -f logs/api.log
```

### Enable Django Logging
Configure in settings.py for detailed request/response logging

## Automated Testing

Use Python requests library for scripted tests:
```python
import requests

url = "http://localhost:8000/api/patients/"
headers = {"Authorization": "Token YOUR_TOKEN"}
response = requests.get(url, headers=headers)
print(response.json())
```

---

**Happy Testing! 🧪**
