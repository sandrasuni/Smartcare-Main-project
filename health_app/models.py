from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, username=None, password=None,*args,**kwargs):
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password")
        user= self.model(
            username=username,
            *args,
            **kwargs)
        user.set_password(password)
        user.is_active=True
        user.save()
        return user

    def create_superuser(self, username, password,email):
        user = self.create_user(
            username=username,
            password=password,
            email=email,
            role=1, 
            is_staff=True,
        )
        user.is_superuser = True
        user.save()
        return user

ROLE_CHOICES = [
    (1, 'Admin'),
    (2, 'Doctor'),
    (3, 'Pharmacist'),
    (4, 'Public Health Nurse'),
    (5, 'ASHA Worker'),
    (6, 'User (Patient)'),
    (7, 'Junior Health Inspector'),
    (8, 'Health Care'),

]

class CustomUser(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.IntegerField(choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def _str_(self):
        return self.username
    
from django.db import models
from .models import CustomUser


from django.db import models

class HealthCareProfile(models.Model):
    TYPE_CHOICES = [
        ('fhc', 'FHC'),
        ('chc', 'CHC'),
        ('phc', 'PHC'),
    ]

    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    h_phone = models.CharField(max_length=15, unique=True)
    h_year_of_experience = models.PositiveIntegerField(default=0)
    admin_approve = models.BooleanField(default=False)
    h_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    h_location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.fk_user.username} - {self.h_type}"

# Doctor Profile
class DoctorProfile(models.Model):
    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fk_healthcare = models.ForeignKey(HealthCareProfile, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    contact_number = models.CharField(max_length=15)
    medical_registration_number = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    qualifications = models.TextField()
    years_of_experience = models.PositiveIntegerField()
    address = models.TextField()
    health_centre_status = models.BooleanField(default=False)

# Pharmacist Profile
class PharmacistProfile(models.Model):
    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fk_healthcare = models.ForeignKey(HealthCareProfile, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    contact_number = models.CharField(max_length=15)
    pharmacy_registration_number = models.CharField(max_length=100)
    qualifications = models.TextField()
    years_of_experience = models.PositiveIntegerField()
    address = models.TextField()
    health_centre_status = models.BooleanField(default=False)

# Public Health Nurse Profile
class PublicHealthNurseProfile(models.Model):
    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fk_healthcare = models.ForeignKey(HealthCareProfile, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    contact_number = models.CharField(max_length=15)
    nursing_license_number = models.CharField(max_length=100)
    qualifications = models.TextField()
    years_of_experience = models.PositiveIntegerField()
    training_in_public_health = models.TextField()
    address = models.TextField()
    health_centre_status = models.BooleanField(default=False)

# ASHA Worker Profile
class ASHAWorkerProfile(models.Model):
    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fk_healthcare = models.ForeignKey(HealthCareProfile, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    contact_number = models.CharField(max_length=15)
    asha_worker_id = models.CharField(max_length=100)
    community_assigned = models.TextField()
    training_details = models.TextField()
    experience_in_health_awareness = models.TextField()
    address = models.TextField()
    health_centre_status = models.BooleanField(default=False)


# Junior Health Inspector Profile
class JuniorHealthInspectorProfile(models.Model):
    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fk_healthcare = models.ForeignKey(HealthCareProfile, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    contact_number = models.CharField(max_length=15)
    inspection_license_number = models.CharField(max_length=100)
    qualifications = models.TextField()
    experience_in_health_inspection = models.TextField()
    address = models.TextField()
    health_centre_status = models.BooleanField(default=False)





from django.core.files.storage import default_storage  # Import default_storage
import numpy as np  # Import NumPy
import face_recognition

def encode_face(image_path):
    """Generate face encodings from an image."""
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    return encodings[0] if encodings else None  # Return the first encoding if a face is found

class DoctImgProfile(models.Model):
    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    face_encoding = models.BinaryField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Override save method to generate and store face encoding."""
        super().save(*args, **kwargs)  # Save image first to get path
        if self.profile_image:
            image_path = default_storage.path(self.profile_image.name)
            encoding = encode_face(image_path)
            if encoding is not None:
                self.face_encoding = np.array(encoding).tobytes()
                super().save(update_fields=["face_encoding"])

    
class NurseImgProfile(models.Model):
    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    face_encoding = models.BinaryField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Override save method to generate and store face encoding."""
        super().save(*args, **kwargs)  # Save image first to get path
        if self.profile_image:
            image_path = default_storage.path(self.profile_image.name)
            encoding = encode_face(image_path)
            if encoding is not None:
                self.face_encoding = np.array(encoding).tobytes()
                super().save(update_fields=["face_encoding"])


class PharmacistImgProfile(models.Model):
    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    face_encoding = models.BinaryField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Override save method to generate and store face encoding."""
        super().save(*args, **kwargs)  # Save image first to get path
        if self.profile_image:
            image_path = default_storage.path(self.profile_image.name)
            encoding = encode_face(image_path)
            if encoding is not None:
                self.face_encoding = np.array(encoding).tobytes()
                super().save(update_fields=["face_encoding"])


  
class AshImgProfile(models.Model):
    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    face_encoding = models.BinaryField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Override save method to generate and store face encoding."""
        super().save(*args, **kwargs)  # Save image first to get path
        if self.profile_image:
            image_path = default_storage.path(self.profile_image.name)
            encoding = encode_face(image_path)
            if encoding is not None:
                self.face_encoding = np.array(encoding).tobytes()
                super().save(update_fields=["face_encoding"])



class PhnImgProfile(models.Model):
    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    face_encoding = models.BinaryField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Override save method to generate and store face encoding."""
        super().save(*args, **kwargs)  # Save image first to get path
        if self.profile_image:
            image_path = default_storage.path(self.profile_image.name)
            encoding = encode_face(image_path)
            if encoding is not None:
                self.face_encoding = np.array(encoding).tobytes()
                super().save(update_fields=["face_encoding"])




class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Attendance for {self.user.username} on {self.date}"




class JhiImgProfile(models.Model):
    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    face_encoding = models.BinaryField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Override save method to generate and store face encoding."""
        super().save(*args, **kwargs)  # Save image first to get path
        if self.profile_image:
            image_path = default_storage.path(self.profile_image.name)
            encoding = encode_face(image_path)
            if encoding is not None:
                self.face_encoding = np.array(encoding).tobytes()
                super().save(update_fields=["face_encoding"])


# Patient Profile
class PatientProfile(models.Model):
    fk_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=15)
    patient_id = models.CharField(max_length=15, unique=True, blank=True)
    status = models.BooleanField(default=False)




from django.utils.timezone import now

class PatientReport(models.Model):
    fk_patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True )
    s_continuous_medication = models.BooleanField(default=False)
    file = models.FileField(upload_to='reports/', blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"{self.title} - {self.patient.patient_id}"
    



class UserMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    
    def __str__(self):
        return self.name

####################################################################################################################
#asha add form

class Household(models.Model):
    fk_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    head_of_household = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
class FamilyMember(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='family_members')
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    occupation = models.CharField(max_length=255, blank=True, null=True)
class ChronicIllness(models.Model):
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='chronic_illnesses')
    illness = models.CharField(max_length=255)
    medications_prescribed = models.TextField()
    following_medication = models.BooleanField(default=False)
class FollowUpPatient(models.Model):
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='follow_ups')
    diagnosis = models.CharField(max_length=255)
    last_checkup_date = models.DateField()
    next_followup_date = models.DateField()
class SanitationHygiene(models.Model):
    household = models.OneToOneField(Household, on_delete=models.CASCADE, related_name='sanitation_hygiene')
    has_toilet = models.BooleanField(default=False)
    has_clean_drinking_water = models.BooleanField(default=False)
    has_handwashing_facility = models.BooleanField(default=False)

class ChildHealth(models.Model):
    family_member = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='child_health')
    child_name = models.CharField(max_length=255, blank=True, null=True)  # Assuming name is a string
    child_age = models.IntegerField( blank=True, null=True)
    birth_weight = models.FloatField( blank=True, null=True)
    immunization_status = models.TextField( blank=True, null=True)
    nutritional_status = models.CharField(max_length=50, choices=[('Normal', 'Normal'), ('Underweight', 'Underweight')], blank=True, null=True)
    vaccination_done = models.BooleanField(default=False)
    vaccination_due_date = models.DateField(blank=True, null=True)

class VisitDetails(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='visits')
    date_time = models.DateTimeField(null=True, blank=True)
    reason_for_visit = models.TextField()
    symptoms_reported = models.TextField(blank=True, null=True)
class PregnantWoman(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='pregnancy_details')
    name=models.CharField(max_length=50, blank=True, null=True)
    expected_delivery_date = models.DateField( blank=True, null=True)
    antenatal_checkups_completed = models.BooleanField(default=False)
class EmergencyReferral(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='emergency_cases')
    critical_health_issue = models.BooleanField(default=False)
    referred_to_health_center = models.BooleanField(default=False)
    referral_details = models.TextField(blank=True, null=True)
class HealthEducation(models.Model):
    visit = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='health_education')
    nutrition = models.BooleanField(default=False)
    breastfeeding = models.BooleanField(default=False)
    family_planning = models.BooleanField(default=False)
    sanitation_hygiene = models.BooleanField(default=False)


#communicable disease

class HealthSurvey(models.Model):
    fk_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='health_surveys')
    location = models.CharField(max_length=255, default="Unknown")

    # Fever Cases
    fever_7_days_or_more_male_5_or_less = models.IntegerField(default=0)
    fever_7_days_or_more_male_above_5 = models.IntegerField(default=0)
    fever_7_days_or_more_female_5_or_less = models.IntegerField(default=0)
    fever_7_days_or_more_female_above_5 = models.IntegerField(default=0)
    fever_less_than_7_days_male_5_or_less = models.IntegerField(default=0)
    fever_less_than_7_days_male_above_5 = models.IntegerField(default=0)
    fever_less_than_7_days_female_5_or_less = models.IntegerField(default=0)
    fever_less_than_7_days_female_above_5 = models.IntegerField(default=0)
    fever_with_rash = models.IntegerField(default=0)
    fever_with_bleeding = models.IntegerField(default=0)
    fever_with_altered_sensorium = models.IntegerField(default=0)

    # Cough Cases
    cough_2_weeks_or_less_with_fever = models.IntegerField(default=0)
    cough_2_weeks_or_less_without_fever = models.IntegerField(default=0)
    cough_more_than_2_weeks_with_fever = models.IntegerField(default=0)
    cough_more_than_2_weeks_without_fever = models.IntegerField(default=0)

    # Diarrhea Cases
    loose_watery_stools_with_blood_less_than_2_weeks = models.IntegerField(default=0)
    loose_watery_stools_without_blood_less_than_2_weeks = models.IntegerField(default=0)

    # Other Diseases
    jaundice_less_than_4_weeks = models.IntegerField(default=0)
    acute_flaccid_paralysis = models.IntegerField(default=0)

    # Malaria Cases
    malaria_vivax_rdt = models.IntegerField(default=0)
    malaria_falciparum_rdt = models.IntegerField(default=0)
    malaria_mixed_rdt = models.IntegerField(default=0)

    # Animal Bites
    animal_bite_snake = models.IntegerField(default=0)
    animal_bite_dog = models.IntegerField(default=0)
    animal_bite_other = models.IntegerField(default=0)

    # Leptospirosis
    leptospirosis_rdt = models.IntegerField(default=0)

    # Summary fields
    total_cases = models.IntegerField(default=0)
    total_deaths = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.total_cases = (
            self.fever_7_days_or_more_male_5_or_less + self.fever_7_days_or_more_male_above_5 +
            self.fever_7_days_or_more_female_5_or_less + self.fever_7_days_or_more_female_above_5 +
            self.fever_less_than_7_days_male_5_or_less + self.fever_less_than_7_days_male_above_5 +
            self.fever_less_than_7_days_female_5_or_less + self.fever_less_than_7_days_female_above_5 +
            self.fever_with_rash + self.fever_with_bleeding + self.fever_with_altered_sensorium +
            self.cough_2_weeks_or_less_with_fever + self.cough_2_weeks_or_less_without_fever +
            self.cough_more_than_2_weeks_with_fever + self.cough_more_than_2_weeks_without_fever +
            self.loose_watery_stools_with_blood_less_than_2_weeks + self.loose_watery_stools_without_blood_less_than_2_weeks +
            self.jaundice_less_than_4_weeks + self.acute_flaccid_paralysis +
            self.malaria_vivax_rdt + self.malaria_falciparum_rdt + self.malaria_mixed_rdt +
            self.animal_bite_snake + self.animal_bite_dog + self.animal_bite_other +
            self.leptospirosis_rdt
        )
        super().save(*args, **kwargs)

    def _str_(self):
        return f"Survey for {self.household.head_of_household}"


#########################################################################################################

from datetime import datetime, timedelta

class MaternalCase(models.Model):
    HIGH = 'High'
    MODERATE = 'Moderate'
    LOW = 'Low'
    
    RISK_FACTORS = [
        (HIGH, 'High'),
        (MODERATE, 'Moderate'),
        (LOW, 'Low'),
    ]
    
    household_name = models.CharField(max_length=100, blank=True, null=True)
    pregnant_member_name = models.CharField(max_length=100, blank=True, null=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    antenatal_checkups = models.BooleanField(default=False)
    
    full_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    husband_name = models.CharField(max_length=100, blank=True, null=True)
    husband_contact_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    last_menstrual_period = models.DateField(blank=True, null=True)
    gestational_age_weeks = models.PositiveIntegerField(blank=True, null=True)
    pregnancy_risk_factor = models.CharField(max_length=10, choices=RISK_FACTORS, blank=True, null=True)
    number_of_pregnancies = models.PositiveIntegerField(blank=True, null=True)
    number_of_live_births = models.PositiveIntegerField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.last_menstrual_period:
            self.expected_delivery_date = self.last_menstrual_period + timedelta(days=280)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.full_name





class MaternalVisitSchedule(models.Model):
    FIRST_TRIMESTER = 'First Trimester'
    SECOND_TRIMESTER = 'Second Trimester'
    THIRD_TRIMESTER = 'Third Trimester'
    POSTNATAL = 'Postnatal'

    VISIT_TYPES = [
        (FIRST_TRIMESTER, 'First Trimester'),
        (SECOND_TRIMESTER, 'Second Trimester'),
        (THIRD_TRIMESTER, 'Third Trimester'),
        (POSTNATAL, 'Postnatal'),
    ]

    SCHEDULED = 'Scheduled'
    COMPLETED = 'Completed'
    MISSED = 'Missed'

    VISIT_STATUSES = [
        (SCHEDULED, 'Scheduled'),
        (COMPLETED, 'Completed'),
        (MISSED, 'Missed'),
    ]

    maternal_case = models.ForeignKey(MaternalCase, on_delete=models.CASCADE, related_name='visit_schedules')
    visit_date = models.DateField(blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPES, blank=True, null=True)
    visit_status = models.CharField(max_length=10, choices=VISIT_STATUSES, blank=True, null=True)

    def __str__(self):
        return f"{self.maternal_case.full_name} - {self.visit_type} on {self.visit_date}"

######################################################################################################################


from django.db import models
from django.utils.timezone import now
from datetime import date

class ChildGrowthRecord(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    IMMUNIZATION_STATUS_CHOICES = [
        ('Up to Date', 'Up to Date'),
        ('Delayed', 'Delayed'),
        ('Missed', 'Missed'),
    ]

    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    fk_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    child_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    guardian_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    
    weight = models.FloatField()  # in kg
    height = models.FloatField()  # in cm
    head_circumference = models.FloatField()  # in cm
    mid_upper_arm_circumference = models.FloatField()  # in cm

    exclusive_breastfeeding_till_6_months = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    complementary_feeding_started = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    vitamin_a_supplementation = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    immunization_status = models.CharField(max_length=20, choices=IMMUNIZATION_STATUS_CHOICES)

    def calculate_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

    def __str__(self):
        return self.child_name



#################################################################


class VaccinationRecord(models.Model):
    VACCINE_CHOICES = [
        ('BCG', 'BCG'),
        ('OPV', 'OPV'),
        ('DTP', 'DTP'),
        ('Measles', 'Measles'),
        ('COVID-19', 'COVID-19'),
        ('OPV-0', 'OPV-0'),
        ('Hep-b', 'Hep-b'),
        ('OPV-1', 'OPV-1'),
        ('Penta-1', 'Penta-1'),
        ('IPV-1', 'IPV-1'),
        ('Rota-1', 'Rota-1'),
        ('PCV-1', 'PCV-1'),
        ('OPV-2', 'OPV-2'),
        ('Penta-2', 'Penta-2'),
        ('Rota-2', 'Rota-2'),
        ('OPV-3', 'OPV-3'),
        ('Penta-3', 'Penta-3'),
        ('IPV-2', 'IPV-2'),
        ('Rota-3', 'Rota-3'),
        ('PCV-2', 'PCV-2'),
        ('MR-1', 'MR-1'),
        ('IPV-3', 'IPV-3'),
        ('PCV-booster', 'PCV-booster'),
        ('Vita-a1', 'Vita-a1'),
        ('JE-1', 'JE-1'),
        ('DPT-booster-1', 'DPT-booster-1'),
        ('Vita-a2', 'Vita-a2'),
        ('MR-2', 'MR-2'),
        ('JE-2', 'JE-2'),
        ('OPV-booster', 'OPV-booster'),
        ('DPT-booster-2', 'DPT-booster-2'),
        ('TD', 'TD'),
    ]

    ROUTE_CHOICES = [
        ('Oral', 'Oral'),
        ('Intramuscular', 'Intramuscular'),
        ('Subcutaneous', 'Subcutaneous'),
    ]
    vaccinator_name = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    patient_name=models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    contact_number = models.CharField(max_length=15)
    location = models.TextField()
    address = models.TextField()
    vaccine_name = models.CharField(max_length=50, choices=VACCINE_CHOICES)
    vaccination_date = models.DateField()
    route_of_administration = models.CharField(max_length=50, choices=ROUTE_CHOICES)
    

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.vaccine_name}"

#######################################################################

from django.db import models

class VaccinationSchedule(models.Model):
    AGE_CHOICES = [
        ('0-1', '0-1 month'),
        ('1.5', '1.5 months'),
        ('2.5', '2.5 months'),
        ('3.5', '3.5 months'),
        ('9', '9 months'),
        ('16-24', '16-24 months'),
        ('5-6', '5-6 years'),
        ('10', '10 years'),
        ('16', '16 years'),
    ]
    gender_choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]

    vaccinator_name = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    vaccination_record = models.ForeignKey(VaccinationRecord, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10,choices=gender_choices)
    age_group = models.CharField(max_length=10, choices=AGE_CHOICES)
    vaccines = models.TextField()  # Store comma-separated vaccine names
    vaccination_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_age_group_display()} - {self.vaccines}"
    


    ############################################

from django.db import models

class Bedridden(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    DEPENDENCY_CHOICES = [
        ('Partial', 'Partial'),
        ('Complete', 'Complete'),
    ]

    fk_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    existing_conditions = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    past_surgeries = models.TextField(blank=True)
    duration_of_bedridden = models.CharField(max_length=100)
    primary_diagnosis = models.CharField(max_length=100)
    level_of_dependency = models.CharField(max_length=10, choices=DEPENDENCY_CHOICES)
    caregiver_name = models.CharField(max_length=100)
    caregiver_contact = models.CharField(max_length=15)
    date_of_registration = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name


###########################################################################################

class BedriddenVisit(models.Model):
    HEALTH_WORKER_CHOICES = [
        ('PHN', 'Public Health Nurse'),
        ('JHI', 'Junior Health Inspector'),
    ]

    fk_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    patient = models.ForeignKey(Bedridden, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    visit_time = models.TimeField()
    assigned_health_worker = models.CharField(max_length=3, choices=HEALTH_WORKER_CHOICES)
    assigned_asha_worker = models.ForeignKey(ASHAWorkerProfile, on_delete=models.SET_NULL, null=True)
    follow_up_required = models.BooleanField(default=False)



#####################################################################

#medicine

class Medicine(models.Model):
    DOSAGE_FORMS = [
        ('Tablet', 'Tablet'),
        ('Capsule', 'Capsule'),
        ('Syrup', 'Syrup'),
        ('Injection', 'Injection'),
        ('Cream', 'Cream'),
    ]

    ROUTES_OF_ADMINISTRATION = [
        ('Oral', 'Oral'),
        ('IV', 'Intravenous'),
        ('IM', 'Intramuscular'),
        ('Topical', 'Topical'),
    ]

    fk_pharmacy= models.ForeignKey(PharmacistProfile,on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    medicine_code = models.CharField(max_length=100)
    drug_code = models.CharField(max_length=100)
    batch_lot_number = models.CharField(max_length=100)
    strength_concentration = models.CharField(max_length=50)
    inactive_ingredients = models.TextField()
    dosage_form = models.CharField(max_length=50, choices=DOSAGE_FORMS)
    route_of_administration = models.CharField(max_length=50, choices=ROUTES_OF_ADMINISTRATION)
    recommended_dosage = models.CharField(max_length=100)
    expiry_date = models.DateField()
    manufacturing_date = models.DateField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    stock_status=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.medicine_name} ({self.brand_name})"
    

    
class Prescription(models.Model):
    DAYS_CHOICES = [
        (1, "1 Day"),
        (2, "2 Days"),
        (3, "3 Days"),
        (4, "4 Days"),
        (5, "5 Days"),
        (6, "6 Days"),
        (7, "1 Week"),
    ]
    TIME_CHOICES = [
        ("3_bf", "3 times before food"),
        ("3_af", "3 times after food"),
        ("2_bf", "2 times before food"),
        ("2_af", "2 times after food"),
        ("1_bf", "1 time before food"),
        ("1_af", "1 time after food"),
    ]

    fk_doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="prescriptions_given")
    fk_patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="prescriptions_received")
    fk_medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    disease_name = models.CharField(max_length=100,null=True,blank=True)
    time_to_take = models.CharField(max_length=10,choices=TIME_CHOICES,default="2_af")
    days_to_take = models.IntegerField(choices=DAYS_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)


class Token_No(models.Model):
    token_number = models.CharField(max_length=250)
    fk_doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="token_doct")
    fk_patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="token_pat")
    created_date = models.DateTimeField(auto_now_add=True)



class Complaint(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"Complaint by {self.user.username}"




##########################################################################################################

class G_Report(models.Model):
    fk_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField()
    report_date = models.DateField()
    reporter_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    INSTITUTE_TYPE_CHOICES = (
        ('government', 'Government'),
        ('private', 'Private'),
    )
    institute_type = models.CharField(max_length=20, choices=INSTITUTE_TYPE_CHOICES)
    health_center = models.ForeignKey(HealthCareProfile, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    institute_name = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=100, blank=True)
    patient_name = models.CharField(max_length=100)
    disease_name = models.CharField(max_length=100)
    symptoms = models.TextField()
    TRANSMISSION_MODE_CHOICES = (
        ('air', 'Air'),
        ('water', 'Water'),
        ('other', 'Other'),
    )
    transmission_mode = models.CharField(max_length=20, choices=TRANSMISSION_MODE_CHOICES)
    ISOLATION_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    isolation = models.CharField(max_length=10, choices=ISOLATION_CHOICES)
    patient_age = models.PositiveIntegerField()
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    patient_gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()

    def __str__(self):
        return f'Report by {self.reporter_name} - {self.patient_name}'



# models.py
from django.db import models
from django.core.mail import send_mail
from django.conf import settings

class SupplyMedicine(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    quantity_issued = models.PositiveIntegerField()
    issued_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    issued_by = models.ForeignKey(PharmacistProfile, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        # Check if this is a new issuance (not an update)
        is_new = self.pk is None
        
        super().save(*args, **kwargs)
        
        if is_new and self.status == 'delivered':
            # Decrease stock quantity
            medicine = self.prescription.fk_medicine
            medicine.stock_quantity -= self.quantity_issued
            medicine.save()
            
            # Check stock level and send email if low
            if medicine.stock_quantity < 30:
                subject = f'Low Stock Alert: {medicine.medicine_name}'
                message = (
                    f'The stock quantity for {medicine.medicine_name} ({medicine.brand_name}) '
                    f'is now {medicine.stock_quantity}, which is below the threshold of 30. '
                    f'Please restock soon.'
                )
                recipient_list = [pharmacist.fk_user.email for pharmacist in PharmacistProfile.objects.all()]
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list,
                    fail_silently=False,
                )
