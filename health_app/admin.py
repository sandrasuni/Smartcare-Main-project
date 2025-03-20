from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    DoctorProfile,
    PharmacistProfile,
    PublicHealthNurseProfile,
    ASHAWorkerProfile,
    PatientProfile,
    JuniorHealthInspectorProfile,
    PatientReport,
    HealthCareProfile
)


class CustomUserAdmin(UserAdmin):
    # Fields to display in the admin user list view
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    
    # Fields to enable filtering by
    list_filter = ('role', 'is_staff', 'is_active')
    
    # Fields to enable search on
    search_fields = ('username', 'email')
    
    # Fieldsets for the detail view
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    # Fields for the 'Add User' form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )
    
    # Default ordering in the admin list view
    ordering = ('email',)

@admin.register(HealthCareProfile)
class HealthCareProfileAdmin(admin.ModelAdmin):
    list_display = ('fk_user', 'h_phone', 'h_year_of_experience', 
                    'admin_approve','h_type','h_location')


# Admin classes for profile models
@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('fk_user','fk_healthcare', 'gender', 'dob', 'contact_number', 'specialization', 'years_of_experience')
    search_fields = ('fk_user__username', 'specialization', 'medical_registration_number')


@admin.register(PharmacistProfile)
class PharmacistProfileAdmin(admin.ModelAdmin):
    list_display = ('fk_user','fk_healthcare','gender', 'dob', 'contact_number', 'pharmacy_registration_number', 'years_of_experience')
    search_fields = ('fk_user__username', 'pharmacy_registration_number')


@admin.register(PublicHealthNurseProfile)
class PublicHealthNurseProfileAdmin(admin.ModelAdmin):
    list_display = ('fk_user','fk_healthcare', 'gender', 'dob', 'contact_number', 'nursing_license_number', 'years_of_experience')
    search_fields = ('fk_user__username', 'nursing_license_number')


@admin.register(ASHAWorkerProfile)
class ASHAWorkerProfileAdmin(admin.ModelAdmin):
    list_display = ('fk_user','fk_healthcare', 'gender', 'dob', 'contact_number', 'asha_worker_id', 'community_assigned')
    search_fields = ('fk_user__username', 'asha_worker_id')


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('fk_user', 'gender', 'dob', 'contact_number', 'patient_id', 'emergency_contact')
    search_fields = ('fk_user__username', 'patient_id')


@admin.register(JuniorHealthInspectorProfile)
class JuniorHealthInspectorProfileAdmin(admin.ModelAdmin):
    list_display = ('fk_user','fk_healthcare', 'gender', 'dob', 'contact_number', 'inspection_license_number', 'experience_in_health_inspection')
    search_fields = ('fk_user__username', 'inspection_license_number')


# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(PatientReport)
class PatientReportAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'title', 'description')

    def get_patient_name(self, obj):
        return obj.fk_patient.fk_user.username  # Replace 'name' with the actual attribute for the patient's name in PatientProfile

    get_patient_name.short_description = 'Patient Name'





from .models import *

@admin.register(DoctImgProfile)
class DoctImgProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_user','profile_image_display')
    search_fields = ('doctor_name', 'fk_user__username')

    def profile_image_display(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return "No Image"
    profile_image_display.short_description = "Profile Image"

@admin.register(NurseImgProfile)
class AshImgProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'fk_user', 'profile_image_display')
    search_fields = ('nurse_name', 'fk_user__username')

    def profile_image_display(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return "No Image"
    profile_image_display.short_description = "Profile Image"

@admin.register(AshImgProfile)
class Admin(admin.ModelAdmin):
    list_display = ('id', 'fk_user', 'profile_image_display')
    search_fields = ('nurse_name', 'fk_user__username')

    def profile_image_display(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return "No Image"
    profile_image_display.short_description = "Profile Image"

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date')
    list_filter = ('date',)
    search_fields = ('user__username',)



from django.contrib import admin
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("fk_doctor", "fk_patient", "fk_medicine", "disease_name", "days_to_take", "created_date")
    search_fields = ("fk_doctor__fk_user__username", "fk_patient__fk_user__username", "fk_medicine__medicine_name", "disease_name")
    list_filter = ("created_date", "days_to_take")
    ordering = ("-created_date",)


from django.contrib import admin
from .models import Token_No

class TokenNoAdmin(admin.ModelAdmin):
    list_display = ('token_number', 'fk_doctor', 'fk_patient', 'created_date')
    search_fields = ('token_number', 'fk_doctor__fk_user__username', 'fk_patient__fk_user__username')
    list_filter = ('created_date',)

admin.site.register(Token_No, TokenNoAdmin)
