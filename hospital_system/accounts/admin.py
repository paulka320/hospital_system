from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fields = ['role', 'department', 'phone_number', 'profile_image', 'bio', 'is_active_staff']
    extra = 0


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_role', 'is_active']
    list_filter = ['is_active', 'profile__role', 'profile__department']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    inlines = [UserProfileInline]

    def get_role(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.get_role_display()
        return 'No Role'
    get_role.short_description = 'Role'


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'role', 'department', 'phone_number', 'is_active_staff', 'created_at']
    list_filter = ['role', 'department', 'is_active_staff']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number']
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Professional Info', {
            'fields': ('role', 'department', 'phone_number')
        }),
        ('Profile Details', {
            'fields': ('profile_image', 'bio')
        }),
        ('Status', {
            'fields': ('is_active_staff', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['user']
        return self.readonly_fields


# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
