from django.contrib import admin
from .models import CustomUser, Song
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    ordering = ('user_name',)
    list_display = (
        'user_name', 'email', 'first_name', 'last_name', 'is_staff',
        'is_doctor', 'group', 'dob', 'address', 'city', 'state', 
        'pincode', 'phone', 'otp', 'profile', 'gender'
        )

    fieldsets = (
        (None, {
            'fields': ('user_name', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('profile', 'is_doctor', 'group', 'gender', 'dob', 'address',
                        'city', 'state', 'pincode', 'phone', 'otp')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('user_name', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('profile', 'is_doctor', 'group', 'gender', 'dob', 'address',
                        'city', 'state', 'pincode', 'phone', 'otp')
        })
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Song)