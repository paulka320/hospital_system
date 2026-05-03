# Database Migration & Data Management Guide

## Understanding Migrations

Django migrations track changes to your database schema. They ensure that your database stays synchronized with your models.

## Creating Migrations

### Create migrations for all changes
```bash
python manage.py makemigrations
```

### Create migrations for specific app
```bash
python manage.py makemigrations patients
python manage.py makemigrations doctors
python manage.py makemigrations appointments
```

### Name your migration
```bash
python manage.py makemigrations patients --name add_blood_type
```

### Check what will be migrated
```bash
python manage.py makemigrations --dry-run
```

## Applying Migrations

### Apply all pending migrations
```bash
python manage.py migrate
```

### Apply migrations for specific app
```bash
python manage.py migrate patients
```

### Apply migrations up to specific point
```bash
python manage.py migrate patients 0002
```

### See migration status
```bash
python manage.py showmigrations
```

## Reversing Migrations

### Reverse all migrations for an app
```bash
python manage.py migrate patients zero
```

### Reverse to specific migration
```bash
python manage.py migrate patients 0001
```

## Viewing Migrations

### Show migration SQL
```bash
python manage.py sqlmigrate patients 0001
```

### List all migrations
```bash
python manage.py showmigrations
```

## Common Migration Issues

### Issue: "django.db.utils.OperationalError: no such table"
**Solution:** 
```bash
python manage.py migrate
```

### Issue: "Migration conflicts"
**Solution:**
```bash
python manage.py makemigrations --merge
```

### Issue: "Existing models not detected"
**Solution:**
- Ensure models.py is properly formatted
- Check for syntax errors
- Verify app is in INSTALLED_APPS

## Model Changes and Migrations

### Adding a New Field
```python
# In models.py
new_field = models.CharField(max_length=100, null=True, blank=True)

# Create and apply migration
python manage.py makemigrations
python manage.py migrate
```

### Changing Field Type
```python
# Before
age = models.IntegerField()

# After
age = models.FloatField()

# Create and apply migration
python manage.py makemigrations
python manage.py migrate
```

### Making Field Required
```python
# Before
email = models.EmailField(null=True, blank=True)

# After
email = models.EmailField()

# Note: You may need to provide a default or set null=False with default value
```

### Adding Unique Constraint
```python
# Before
phone = models.CharField(max_length=15)

# After
phone = models.CharField(max_length=15, unique=True)
```

### Removing a Field
```python
# Remove from models.py and run:
python manage.py makemigrations
python manage.py migrate
```

## Data Management

### Export Data to JSON
```bash
# Export all data
python manage.py dumpdata > backup.json

# Export specific app
python manage.py dumpdata patients > patients_backup.json

# Export specific model
python manage.py dumpdata patients.Patient > patients_only.json

# Pretty print
python manage.py dumpdata --indent 2 > backup.json
```

### Import Data from JSON
```bash
python manage.py loaddata backup.json
python manage.py loaddata patients_backup.json
```

### Clear Data
```bash
# Delete all data (keep migrations)
python manage.py flush

# Delete specific app data
python manage.py flush --no-input
```

## Django Shell Operations

### Access Django Shell
```bash
python manage.py shell
```

### Create Objects
```python
from patients.models import Patient
from datetime import date

patient = Patient.objects.create(
    name="John Doe",
    date_of_birth=date(1990, 5, 15),
    age=34,
    gender="M",
    phone="+234800000000",
    email="john@example.com"
)
```

### Query Objects
```python
from patients.models import Patient

# Get all patients
patients = Patient.objects.all()

# Get specific patient
patient = Patient.objects.get(id=1)

# Filter patients
patients = Patient.objects.filter(gender="M")

# Count records
count = Patient.objects.count()

# Order by
patients = Patient.objects.order_by('-created_at')
```

### Update Objects
```python
patient = Patient.objects.get(id=1)
patient.phone = "+234900000000"
patient.save()

# Bulk update
Patient.objects.filter(gender="M").update(age=F('age') + 1)
```

### Delete Objects
```python
patient = Patient.objects.get(id=1)
patient.delete()

# Bulk delete
Patient.objects.filter(is_active=False).delete()
```

## Database Backup and Restore

### SQLite Backup
```bash
# Copy the database file
cp db.sqlite3 db.sqlite3.backup

# Or with timestamp
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d)
```

### PostgreSQL Backup
```bash
# Backup database
pg_dump hospital_db > hospital_backup.sql

# Backup with compression
pg_dump hospital_db | gzip > hospital_backup.sql.gz

# Restore from backup
psql hospital_db < hospital_backup.sql

# Restore from compressed
gunzip -c hospital_backup.sql.gz | psql hospital_db
```

## Database Optimization

### Run Database Checks
```bash
python manage.py check
```

### View Query Logs
```python
from django.db import connection

# In Django shell
for query in connection.queries:
    print(query)
```

### Analyze Slow Queries
```bash
python manage.py shell_plus

# Then use Django Debug Toolbar or logging
```

### Vacuumize Database (SQLite)
```bash
python manage.py shell
>>> from django.db import connection
>>> connection.cursor().execute('VACUUM;')
```

## Scaling the Database

### Switch to PostgreSQL (Recommended for Production)

1. **Install PostgreSQL and psycopg2**
```bash
pip install psycopg2-binary
```

2. **Update settings.py**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hospital_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Migrate data**
```bash
# Export from SQLite
python manage.py dumpdata --indent 2 > data.json

# Migrate database
python manage.py migrate

# Load data into PostgreSQL
python manage.py loaddata data.json
```

## Monitoring Migrations

### Check Migration History
```bash
python manage.py showmigrations --list
```

### Get Migration Details
```bash
python manage.py sqlmigrate patients 0001
```

### Test Migrations Without Applying
```bash
python manage.py migrate --plan
```

## Best Practices

1. **Always create migrations after model changes**
   ```bash
   python manage.py makemigrations
   ```

2. **Review migrations before applying**
   ```bash
   python manage.py sqlmigrate patients 0001
   ```

3. **Test migrations on development first**
   - Test locally
   - Test on staging
   - Then deploy to production

4. **Keep backups**
   ```bash
   python manage.py dumpdata > backup.json
   ```

5. **Document custom migrations**
   - Add comments to migration files
   - Explain why changes were needed

6. **Use meaningful migration names**
   ```bash
   python manage.py makemigrations patients --name add_blood_type
   ```

7. **Never edit applied migrations**
   - Create new migration if needed
   - Use makemigrations to generate new migration

8. **Test data integrity**
   ```python
   # In migration operations
   def check_data(apps, schema_editor):
       Patient = apps.get_model('patients', 'Patient')
       # Verify data...
   ```

## Common Database Queries

### Get all patients with their appointments
```python
from patients.models import Patient

patients = Patient.objects.prefetch_related('appointments').all()
```

### Get doctors with most appointments
```python
from django.db.models import Count
from doctors.models import Doctor

doctors = Doctor.objects.annotate(
    appointment_count=Count('appointments')
).order_by('-appointment_count')
```

### Get pending bills
```python
from billing.models import Bill

pending_bills = Bill.objects.filter(status='issued')
```

### Get today's appointments
```python
from datetime import date
from appointments.models import Appointment

today_appointments = Appointment.objects.filter(date=date.today())
```

## Troubleshooting

### Issue: "ProgrammingError: column doesn't exist"
**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: "IntegrityError: UNIQUE constraint failed"
**Solution:**
- Check for duplicate data
- Remove duplicates before migration
- Or handle in data migration

### Issue: "Failed to create migration"
**Solution:**
- Check model syntax
- Verify app is in INSTALLED_APPS
- Try: `python manage.py makemigrations --empty patients --name fix_issue`

---

**For more help:** `python manage.py help migrate`
