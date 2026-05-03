from django.contrib.auth.models import User
from .models import Notification


def create_notification(user, notification_type, title, message, content_type=None, object_id=None):
    """
    Create a notification for a user.
    
    Args:
        user: User object
        notification_type: Type of notification
        title: Notification title
        message: Notification message
        content_type: Optional content type (e.g., 'appointment', 'bill')
        object_id: Optional related object ID
    """
    notification = Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        content_type=content_type,
        object_id=object_id
    )
    return notification


def send_appointment_reminder(appointment):
    """Send appointment reminder notification"""
    from appointments.models import Appointment
    
    # Create notification for patient
    if appointment.patient.user:
        create_notification(
            user=appointment.patient.user,
            notification_type='appointment_reminder',
            title=f'Appointment Reminder',
            message=f'You have an appointment with Dr. {appointment.doctor.name} on {appointment.date} at {appointment.time}',
            content_type='appointment',
            object_id=appointment.id
        )
    
    # Create notification for doctor
    if appointment.doctor.user:
        create_notification(
            user=appointment.doctor.user,
            notification_type='appointment_reminder',
            title=f'Upcoming Appointment',
            message=f'You have an appointment with {appointment.patient.name} on {appointment.date} at {appointment.time}',
            content_type='appointment',
            object_id=appointment.id
        )


def send_lab_result_ready(laboratory):
    """Send lab result ready notification"""
    if laboratory.patient.user:
        create_notification(
            user=laboratory.patient.user,
            notification_type='lab_result_ready',
            title='Lab Result Ready',
            message=f'Your {laboratory.get_test_type_display()} result is ready. Please contact us or visit our portal to view the results.',
            content_type='laboratory',
            object_id=laboratory.id
        )


def send_bill_issued(bill):
    """Send bill issued notification"""
    if bill.patient.user:
        create_notification(
            user=bill.patient.user,
            notification_type='bill_issued',
            title='New Bill Generated',
            message=f'A new bill (#{bill.bill_number}) has been generated for ₦{bill.total_amount}. Payment due on {bill.due_date}.',
            content_type='bill',
            object_id=bill.id
        )
