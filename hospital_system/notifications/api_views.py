from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Notification, NotificationPreference
from .serializers import NotificationSerializer, NotificationPreferenceSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Notifications.
    
    Endpoints:
    - GET /api/notifications/ - List user's notifications
    - GET /api/notifications/unread/ - Get unread notifications
    - POST /api/notifications/{id}/mark-as-read/ - Mark notification as read
    - POST /api/notifications/mark-all-read/ - Mark all notifications as read
    - GET /api/notifications/preferences/ - Get notification preferences
    - PUT /api/notifications/preferences/ - Update notification preferences
    """
    
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Only return notifications for the current user"""
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get all unread notifications for the current user"""
        notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).order_by('-created_at')
        
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        
        return Response(
            {'status': 'Notification marked as read'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read for the current user"""
        from django.utils import timezone
        unread_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response(
            {'status': f'{unread_count} notifications marked as read'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get', 'put'])
    def preferences(self, request):
        """Get or update notification preferences"""
        try:
            preferences = NotificationPreference.objects.get(user=request.user)
        except NotificationPreference.DoesNotExist:
            preferences = NotificationPreference.objects.create(user=request.user)
        
        if request.method == 'PUT':
            serializer = NotificationPreferenceSerializer(preferences, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = NotificationPreferenceSerializer(preferences)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        """Delete all notifications for the current user"""
        count = Notification.objects.filter(user=request.user).delete()[0]
        return Response(
            {'status': f'{count} notifications deleted'},
            status=status.HTTP_200_OK
        )
