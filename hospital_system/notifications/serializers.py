from rest_framework import serializers
from .models import Notification, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'user', 'title', 'message',
            'is_read', 'read_at', 'content_type', 'object_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'read_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = [
            'user', 'email_notifications', 'sms_notifications', 'push_notifications',
            'appointment_reminders', 'lab_results', 'billing_alerts', 'prescription_alerts', 'updated_at'
        ]
        read_only_fields = ['user', 'updated_at']
