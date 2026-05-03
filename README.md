# Hospital Management System

A comprehensive Django-based hospital management system with advanced features for patient management, doctor scheduling, appointments, medical records, billing, and notifications.

## Features

### 🏥 Patient Management
- Complete patient profiles with comprehensive health information
- Blood type and allergies tracking
- Emergency contact information
- Insurance provider management
- Medical history and records

### 👨‍⚕️ Doctor Management
- Doctor profiles with specialization and qualifications
- Availability scheduling (working hours per day)
- Patient ratings and reviews
- Consultation fees management
- Experience tracking

### 📅 Appointment Management
- Advanced appointment scheduling system
- Multiple appointment types (consultation, follow-up, surgery, emergency)
- Appointment status tracking (scheduled, confirmed, completed, cancelled, rescheduled)
- Appointment reminders and notifications
- Reschedule functionality
- Calendar-based scheduling

### 📋 Medical Records
- Complete medical record management
- Diagnosis and disease tracking
- Prescription management with dosage information
- Visit history with vital signs tracking
- Lab test results

### 🔬 Laboratory Management
- Multiple test types (blood, malaria, COVID-19, urine, X-ray, ultrasound, CT scan, ECG)
- Test request and completion tracking
- Result documentation
- Technician notes

### 💊 Prescription Management
- Digital prescription system
- Dosage and frequency management
- Prescription status tracking (active, completed, filled, cancelled)
- Medicine tracking

### 💰 Billing System
- Comprehensive billing with invoicing
- Multiple bill items with categorization
- Tax and discount management
- Payment tracking with multiple payment methods
- Payment status management

### 🔔 Notification System
- Real-time notifications
- Multiple notification types (appointments, lab results, billing, prescriptions)
- User notification preferences
- Email/SMS/Push notification support
- Read/unread tracking

### 🔐 Security & Access Control
- Role-based access control (Doctor, Reception, Admin)
- User authentication and authorization
- Login/logout functionality
- Secure password management

### 📱 REST API
- Comprehensive REST API with ViewSets
- Full CRUD operations for all models
- Advanced filtering and search capabilities
- Pagination support
- Authentication required for all endpoints

## Installation

### Prerequisites
- Python 3.8+
- Django 6.0+
- PostgreSQL or SQLite (default)

### Setup Instructions

1. **Clone the repository**
```bash
git clone <repository-url>
cd hospital_system
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database**
- Update `hospital_system/settings.py` with your database configuration
- Default is SQLite (suitable for development)

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Load initial data (optional)**
```bash
python manage.py loaddata fixtures/initial_data.json
```

8. **Run development server**
```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`

## Project Structure

```
hospital_system/
├── hospital_system/          # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── accounts/                 # User authentication
├── patients/                 # Patient management
│   ├── models.py            # Patient, MedicalRecord, Visit, Laboratory, Prescription
│   ├── views.py             # Web views
│   ├── api_views.py         # REST API views
│   ├── serializers.py       # DRF serializers
│   └── forms.py             # Django forms
├── doctors/                  # Doctor management
│   ├── models.py            # Doctor, DoctorAvailability, DoctorReview
│   ├── views.py             # Web views
│   ├── api_views.py         # REST API views
│   ├── serializers.py       # DRF serializers
│   └── forms.py             # Django forms
├── appointments/            # Appointment management
│   ├── models.py            # Appointment model
│   ├── views.py             # Web views
│   ├── api_views.py         # REST API views
│   └── serializers.py       # DRF serializers
├── billing/                 # Billing management
│   ├── models.py            # Bill, BillItem, Payment models
│   ├── views.py             # Web views
│   ├── api_views.py         # REST API views
│   └── serializers.py       # DRF serializers
├── notifications/           # Notification system
│   ├── models.py            # Notification, NotificationPreference
│   ├── views.py             # Web views
│   ├── api_views.py         # REST API views
│   ├── serializers.py       # DRF serializers
│   ├── services.py          # Notification services
│   └── admin.py             # Admin configuration
├── dashboard/               # Dashboard views
├── core/                    # Core utilities
│   └── utils.py             # Helper functions
├── api/                     # API configuration
│   └── urls.py              # API URL routing
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS)
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```

## API Endpoints

### Authentication
```
POST   /accounts/login/       - Login
GET    /accounts/logout/      - Logout
```

### Patients
```
GET    /api/patients/                      - List all patients
POST   /api/patients/                      - Create new patient
GET    /api/patients/{id}/                 - Get patient detail
PUT    /api/patients/{id}/                 - Update patient
DELETE /api/patients/{id}/                 - Delete patient
GET    /api/patients/{id}/medical-records/ - Get medical records
GET    /api/patients/{id}/visits/          - Get visits
GET    /api/patients/{id}/labs/            - Get lab tests
GET    /api/patients/{id}/prescriptions/   - Get prescriptions
```

### Doctors
```
GET    /api/doctors/                       - List all doctors
POST   /api/doctors/                       - Create new doctor
GET    /api/doctors/{id}/                  - Get doctor detail
GET    /api/doctors/search/                - Search doctors
GET    /api/doctors/{id}/availability/    - Get availability
GET    /api/doctors/{id}/reviews/          - Get reviews
GET    /api/doctors/{id}/appointments/    - Get appointments
```

### Appointments
```
GET    /api/appointments/                  - List all appointments
POST   /api/appointments/                  - Create new appointment
GET    /api/appointments/{id}/             - Get appointment detail
PUT    /api/appointments/{id}/             - Update appointment
DELETE /api/appointments/{id}/             - Delete appointment
GET    /api/appointments/upcoming/         - Get upcoming appointments
GET    /api/appointments/today/            - Get today's appointments
POST   /api/appointments/{id}/confirm/     - Confirm appointment
POST   /api/appointments/{id}/cancel/      - Cancel appointment
POST   /api/appointments/{id}/reschedule/  - Reschedule appointment
```

### Medical Records
```
GET    /api/medical-records/               - List all records
POST   /api/medical-records/               - Create new record
GET    /api/medical-records/{id}/          - Get record detail
PUT    /api/medical-records/{id}/          - Update record
DELETE /api/medical-records/{id}/          - Delete record
```

### Prescriptions
```
GET    /api/prescriptions/                 - List all prescriptions
POST   /api/prescriptions/                 - Create new prescription
GET    /api/prescriptions/{id}/            - Get prescription detail
PUT    /api/prescriptions/{id}/            - Update prescription
POST   /api/prescriptions/{id}/mark-filled/ - Mark as filled
```

### Notifications
```
GET    /api/notifications/                 - List user's notifications
GET    /api/notifications/unread/          - Get unread notifications
POST   /api/notifications/{id}/mark-as-read/ - Mark as read
POST   /api/notifications/mark-all-read/   - Mark all as read
GET    /api/notifications/preferences/    - Get preferences
PUT    /api/notifications/preferences/    - Update preferences
DELETE /api/notifications/delete-all/     - Delete all notifications
```

## Usage Examples

### Create a Patient (API)
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
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

### Create an Appointment (API)
```bash
curl -X POST http://localhost:8000/api/appointments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "patient": 1,
    "doctor": 1,
    "date": "2026-05-15",
    "time": "10:00:00",
    "appointment_type": "consultation",
    "reason": "General checkup"
  }'
```

### Get Upcoming Appointments (API)
```bash
curl -X GET http://localhost:8000/api/appointments/upcoming/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## Admin Panel

Access the Django admin panel at `/admin/` with superuser credentials to:
- Manage patients, doctors, and appointments
- View and manage medical records
- Process billing
- View notifications
- Manage user accounts and permissions

## Testing

Run tests with:
```bash
python manage.py test
```

Run specific test module:
```bash
python manage.py test patients.tests
```

## Performance Optimizations

- Database indexes on frequently queried fields
- Related_name usage for reverse relationships
- Query optimization with select_related and prefetch_related
- Pagination support in APIs
- Caching recommendations for high-traffic endpoints

## Security Considerations

- Always use environment variables for sensitive data (SECRET_KEY, database credentials)
- Enable HTTPS in production
- Set DEBUG = False in production
- Use strong SECRET_KEY
- Implement CORS properly
- Validate all user inputs
- Use parameterized queries (Django ORM prevents SQL injection by default)

## Future Enhancements

- SMS/Email notifications integration
- Mobile application
- Online consultation video integration
- Advanced analytics and reporting
- Prescription printing/PDF generation
- Insurance claim management
- Emergency services integration
- Staff management system
- Inventory management for pharmacy
- Medical equipment scheduling

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests for new features
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue on the repository.

## Contact

For more information, contact: support@hospitalsystem.com
