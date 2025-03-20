from django.shortcuts import render,redirect
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages

# Create your views here.

def landing_page(request):
    return render(request,'dashboard/landing.html')

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .models import HealthCareProfile, DoctorProfile, PharmacistProfile, PublicHealthNurseProfile, ASHAWorkerProfile, PatientProfile, JuniorHealthInspectorProfile

def all_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Define a dictionary to map roles to their corresponding profile models
            role_profiles = {
                2: DoctorProfile,
                3: PharmacistProfile,
                4: PublicHealthNurseProfile,
                5: ASHAWorkerProfile,
                6: PatientProfile,
                7: JuniorHealthInspectorProfile,
                8: HealthCareProfile  # For HealthCareProfile role
            }
            # Check if the user has a profile and if their status is active
            if user.role in role_profiles:
                profile_model = role_profiles[user.role]
                try:
                    profile = profile_model.objects.get(fk_user=user)

                    # Check if profile is HealthCareProfile and admin_approve is False
                    if isinstance(profile, HealthCareProfile) and not profile.admin_approve:
                        messages.error(request, "Your account is not approved by the admin. Contact the administrator.")
                        return redirect('all_login')

                    # Only check status for profiles that have it (excluding HealthCareProfile)
                    if hasattr(profile, 'health_centre_status') and not profile.health_centre_status:
                        messages.error(request, "Your healthcare center is deactivated. Contact the administrator.")
                        return redirect('all_login')
                    
                except profile_model.DoesNotExist:
                    messages.error(request, "Profile not found. Contact the administrator.")
                    return redirect('all_login')

            # Log the user in
            login(request, user)

            # Redirect based on user role
            role_redirects = {
                1: 'admin_dashboard',
                2: 'doctor_dashboard',
                3: 'pharmacist_dashboard',
                4: 'public_health_nurse_dashboard',
                5: 'asha_worker_dashboard',
                6: 'patient_dashboard',
                7: 'junior_health_inspector_dashboard',
                8: 'health_dashboard'  # Redirect to health dashboard if it's a HealthCareProfile
            }

            return redirect(role_redirects.get(user.role, 'unknown_role_dashboard'))

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('all_login')  # Redirect back to login page

    return render(request, 'register/all_login.html')

def all_register_page(req):
    return render(req,'register/reg.html')

def register_healthcare(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = 8  # Assuming role 3 is for healthcare professionals

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register_healthcare')

        # Create the user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        # Create healthcare profile
        HealthCareProfile.objects.create(
            fk_user=user,
            h_phone=request.POST.get('h_phone'),
            h_year_of_experience=request.POST.get('h_year_of_experience'),
            h_type=request.POST.get('h_type'),
            h_location=request.POST.get('h_location'),
            admin_approve=False  # Directly setting app_status to False
        )
        return redirect('all_login')

    return render(request, 'register/register_healthcare.html')



def register_doctor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = 2  # Doctor

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register_doctor') 
        
        # Create user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        selected_healthcare = HealthCareProfile.objects.get(id=request.POST.get('fk_healthcare'))

        # Create doctor profile
        DoctorProfile.objects.create(
            fk_user=user,
            fk_healthcare=selected_healthcare,
            gender=request.POST.get('gender'),
            dob=request.POST.get('dob'),
            contact_number=request.POST.get('contact_number'),
            medical_registration_number=request.POST.get('medical_registration_number'),
            specialization=request.POST.get('specialization'),
            qualifications=request.POST.get('qualifications'),
            years_of_experience=request.POST.get('years_of_experience'),
            address=request.POST.get('address'),
            health_centre_status=False  # Default value
        )

        return redirect('all_login')
    approved_healthcare = HealthCareProfile.objects.filter(admin_approve=True)
    
    return render(request, 'register/register_doctor.html',{'approved_healthcare': approved_healthcare})



def register_pharmacist(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = 3  # Pharmacist

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register_pharmacist') 

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        selected_healthcare = HealthCareProfile.objects.get(id=request.POST.get('fk_healthcare'))

        PharmacistProfile.objects.create(
            fk_user=user,
            fk_healthcare=selected_healthcare,
            gender=request.POST.get('gender'),
            dob=request.POST.get('dob'),
            contact_number=request.POST.get('contact_number'),
            pharmacy_registration_number=request.POST.get('pharmacy_registration_number'),
            qualifications=request.POST.get('qualifications'),
            years_of_experience=request.POST.get('years_of_experience'),
            address=request.POST.get('address'),
            health_centre_status=False  # Default value
        )

        return redirect('all_login')
    approved_healthcare = HealthCareProfile.objects.filter(admin_approve=True)

    return render(request, 'register/register_pharmacist.html',{'approved_healthcare': approved_healthcare})


def register_public_health_nurse(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = 4  # Public Health Nurse

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register_public_health_nurse')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        selected_healthcare = HealthCareProfile.objects.get(id=request.POST.get('fk_healthcare'))

        PublicHealthNurseProfile.objects.create(
            fk_user=user,
            fk_healthcare=selected_healthcare,
            gender=request.POST.get('gender'),
            dob=request.POST.get('dob'),
            contact_number=request.POST.get('contact_number'),
            nursing_license_number=request.POST.get('nursing_license_number'),
            qualifications=request.POST.get('qualifications'),
            years_of_experience=request.POST.get('years_of_experience'),
            training_in_public_health=request.POST.get('training_in_public_health'),
            address=request.POST.get('address'),
            health_centre_status=False   # Default value
        )

        return redirect('all_login')
    approved_healthcare = HealthCareProfile.objects.filter(admin_approve=True)

    return render(request, 'register/register_public_health_nurse.html',{'approved_healthcare': approved_healthcare})





def register_asha_worker(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = 5  # ASHA Worker

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register_asha_worker')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        selected_healthcare = HealthCareProfile.objects.get(id=request.POST.get('fk_healthcare'))

        ASHAWorkerProfile.objects.create(
            fk_user=user,
            fk_healthcare=selected_healthcare,
            gender=request.POST.get('gender'),
            dob=request.POST.get('dob'),
            contact_number=request.POST.get('contact_number'),
            asha_worker_id=request.POST.get('asha_worker_id'),
            community_assigned=request.POST.get('community_assigned'),
            training_details=request.POST.get('training_details'),
            experience_in_health_awareness=request.POST.get('experience_in_health_awareness'),
            address=request.POST.get('address'),
            health_centre_status=False   # Default value
        )

        return redirect('all_login')
    approved_healthcare = HealthCareProfile.objects.filter(admin_approve=True)

    return render(request, 'register/register_asha_worker.html',{'approved_healthcare': approved_healthcare})



from django.utils.timezone import now
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser, PatientProfile

import random

def generate_patient_id():
    while True:
        patient_id = f"PAT{random.randint(1000000, 9999999)}"
        if not PatientProfile.objects.filter(patient_id=patient_id).exists():
            return patient_id

def register_patient(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        dob = request.POST.get('dob')
        role = 6  # Patient

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register_patient')

        # Validate Date of Birth (no future dates)
        if dob and dob > str(now().date()):
            messages.error(request, "Date of Birth cannot be in the future!")
            return redirect('register_patient')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        patient_id = generate_patient_id()

        PatientProfile.objects.create(
            fk_user=user,
            gender=request.POST.get('gender'),
            dob=dob,
            contact_number=request.POST.get('contact_number'),
            address=request.POST.get('address'),
            emergency_contact=request.POST.get('emergency_contact'),
            patient_id=patient_id,
            status=True  # Default value
        )

        return redirect('all_login')

    return render(request, 'register/register_patient.html', {'today_date': now().date().isoformat()})




def register_junior_health_inspector(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = 7  # Junior Health Inspector

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register_junior_health_inspector')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        selected_healthcare = HealthCareProfile.objects.get(id=request.POST.get('fk_healthcare'))

        JuniorHealthInspectorProfile.objects.create(
            fk_user=user,
            fk_healthcare=selected_healthcare,
            gender=request.POST.get('gender'),
            dob=request.POST.get('dob'),
            contact_number=request.POST.get('contact_number'),
            inspection_license_number=request.POST.get('inspection_license_number'),
            qualifications=request.POST.get('qualifications'),
            experience_in_health_inspection=request.POST.get('experience_in_health_inspection'),
            address=request.POST.get('address'),
            health_centre_status=False   # Default value
        )

        return redirect('all_login')
    approved_healthcare = HealthCareProfile.objects.filter(admin_approve=True)

    return render(request, 'register/register_junior_health_inspector.html',{'approved_healthcare': approved_healthcare}) 


def admin_dashboard(requset):
    user = requset.user
    return render(requset,'admin/dashboard_admin.html',{'user':user})

def health_dashboard(requset):
    user = requset.user
    return render(requset,'dashboard/dashboard_health.html',{'user':user})


def ashaworker_dashboard(requset):
    user = requset.user
    return render(requset,'asha/dashboard_asha.html',{'user':user})

def doctor_dashboard(requset):
    user = requset.user
    return render(requset,'doctor/dashboard_doctor.html',{'user':user})

def junior_health_dashboard(requset):
    user = requset.user
    return render(requset,'jhi/dashboard_jhi.html',{'user':user})

def patient_dashboard(requset):
    user = requset.user
    patient_profile = PatientProfile.objects.get(fk_user=user)
    return render(requset,'patients/dashboard_patient.html',{'user':user,'patient_profile':patient_profile})

def pharmacist_dashboard(requset):
    user = requset.user
    return render(requset,'pharmacist/dashboard_pharmacist.html',{'user':user})

def public_nurse_dashboard(requset):
    user = requset.user
    return render(requset,'phn/dashboard_phn.html',{'user':user})



def logout_view(request):
    logout(request)
    return redirect('all_login')



from django.shortcuts import render
from .models import ASHAWorkerProfile, DoctorProfile

def list_healthcare(request):
    hp = HealthCareProfile.objects.all()
    return render(request, 'admin/list_healthcare.html', {'health': hp})

def list_asha(request):
    asha_workers = ASHAWorkerProfile.objects.all()
    return render(request, 'admin/list_asha.html', {'asha_workers': asha_workers})

def list_doctors(request):
    doctors = DoctorProfile.objects.all()
    return render(request, 'admin/list_doctors.html', {'doctors': doctors})


# View to list Public Health Nurses
def list_public_health_nurses(request):
    public_health_nurses = PublicHealthNurseProfile.objects.all()
    return render(request, 'admin/list_phn.html', {'public_health_nurses': public_health_nurses})

# View to list Patients
def list_patients(request):
    patients = PatientProfile.objects.all()
    return render(request, 'admin/list_patient.html', {'patients': patients})

# View to list Pharmacists
def list_pharmacists(request):
    pharmacists = PharmacistProfile.objects.all()
    return render(request, 'admin/list_pharmasicst.html', {'pharmacists': pharmacists})

# View to list Junior Health Inspectors
def list_junior_health_inspectors(request):
    junior_health_inspectors = JuniorHealthInspectorProfile.objects.all()
    return render(request, 'admin/list_jhi.html', {'junior_health_inspectors': junior_health_inspectors})





from django.shortcuts import render, redirect
from .models import PatientReport

def patient_report_create(request):
    user = request.user
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')  # Handles file uploads
        is_continuous_medication = request.POST.get('is_continuous_medication') == 'on'
        
        # Directly fetch the associated PatientProfile
        patient_profile = PatientProfile.objects.get(fk_user=user)  # Assuming CustomUser has a related PatientProfile

        # Create and save the report
        report = PatientReport(
            fk_patient=patient_profile,  # Correct link to PatientProfile
            title=title,
            description=description,
            file=file,
            s_continuous_medication=is_continuous_medication  # Save checkbox value
        )
        report.save()
        return redirect('patient_report_list')
    patient_profile = PatientProfile.objects.get(fk_user=user)

    
    return render(request, 'patients/patient_report.html',{'patient_profile':patient_profile})


def patient_report_list(request):
    user = request.user
    reports = PatientReport.objects.filter(fk_patient__fk_user=user)  # Use .filter() to get a queryset
    patient_profile = PatientProfile.objects.get(fk_user=user)

    return render(request, 'patients/report_list.html', {'reports': reports,'patient_profile':patient_profile})


from django.shortcuts import render, get_object_or_404, redirect
from .models import PatientReport

def report_update(request, report_id):
    report = get_object_or_404(PatientReport, id=report_id)

    if request.method == "POST":
        report.title = request.POST.get('title', report.title)
        report.description = request.POST.get('description', report.description)
        report.s_continuous_medication = 'is_continuous_medication' in request.POST

        if 'file' in request.FILES:
            report.file = request.FILES['file']

        report.save()
        return redirect('patient_report_list')  # Change 'some_success_page' to your redirect page

    return render(request, 'patients/update_report.html', {'report': report})

def remove_report(request, report_id):
    report = get_object_or_404(PatientReport, id=report_id)
    report.delete()
    return redirect('patient_report_list')


from django.shortcuts import render, get_object_or_404
from .models import PatientProfile, PatientReport

def search_doctor_patients(request):
    reports = None
    patient = None

    if request.method == "GET" and 'patient_id' in request.GET:
        patient_id = request.GET.get('patient_id')
        try:
            # Fetch the patient by their patient_id
            patient = PatientProfile.objects.get(patient_id=patient_id)
            # Fetch all reports for this patient
            reports = PatientReport.objects.filter(fk_patient=patient)
        except PatientProfile.DoesNotExist:
            # If no patient is found, set patient to None
            patient = None

    return render(request, 'doctor/search_patients.html', {
        'patient': patient,
        'reports': reports,
    })



from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f"/reset_password/{uid}/{token}/")

            # Send reset email
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link to reset your password: {reset_url}",
                from_email=None,  # Use DEFAULT_FROM_EMAIL
                recipient_list=[email],
            )

            messages.success(request, "A password reset link has been sent to your email.")
            return render(request, 'register/forgot_password.html', {'success_message': "A password reset link has been sent to your email."})
        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
            return render(request, 'register/forgot_password.html', {'error_message': "No account found with that email."})

    return render(request, 'register/forgot_password.html')


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password has been reset successfully.")
                return redirect('all_login')
            else:
                messages.error(request, "Passwords do not match.")
                return redirect(request.path)

        return render(request, 'register/reset_password.html')
    else:
        messages.error(request, "Invalid or expired token.")
        return redirect('forgot_password')


def health_status(request,id):
    single_user=HealthCareProfile.objects.get(id=id)
    if single_user:
        single_user.admin_approve = not single_user.admin_approve
        single_user.save()
    return redirect('list_healthcare')


def ash_status(request,id):
    single_user=ASHAWorkerProfile.objects.get(id=id)
    if single_user:
        single_user.health_centre_status = not single_user.health_centre_status
        single_user.save()
    return redirect('h_list_asha')

def patient_status(request,id):  
    single_user=PatientProfile.objects.get(id=id)
    if single_user:
        single_user.status = not single_user.status
        single_user.save()
    return redirect('list_patients')


def jhn_status(request,id):
    single_user=JuniorHealthInspectorProfile.objects.get(id=id)
    if single_user:
        single_user.health_centre_status = not single_user.health_centre_status
        single_user.save()
    return redirect('h_list_inspectors')



def phn_status(request,id):
    single_user=PublicHealthNurseProfile.objects.get(id=id)
    if single_user:
        single_user.health_centre_status = not single_user.health_centre_status
        single_user.save()
    return redirect('h_list_nurse')


def doctor_status(request,id):
    single_user=DoctorProfile.objects.get(id=id)
    if single_user:
        single_user.health_centre_status = not single_user.health_centre_status
        single_user.save()
    return redirect('h_list_doctors')


def pharmacist_status(request,id):
    single_user=PharmacistProfile.objects.get(id=id)
    if single_user:
        single_user.health_centre_status = not single_user.health_centre_status
        single_user.save()
    return redirect('h_list_pharmacists')







def health_list_asha(request):
    user = request.user
    asha_workers = ASHAWorkerProfile.objects.filter(fk_healthcare__fk_user=user)
    return render(request, 'health/list_asha.html', {'asha_workers': asha_workers})

def health_list_doctors(request):
    doctors = DoctorProfile.objects.filter(fk_healthcare__fk_user=request.user)
    return render(request, 'health/list_doctors.html', {'doctors': doctors})


# View to list Public Health Nurses
def health_list_public_health_nurses(request):
    public_health_nurses = PublicHealthNurseProfile.objects.filter(fk_healthcare__fk_user=request.user)
    return render(request, 'health/list_phn.html', {'public_health_nurses': public_health_nurses})


# View to list Pharmacists
def health_list_pharmacists(request):
    pharmacists = PharmacistProfile.objects.filter(fk_healthcare__fk_user=request.user)
    return render(request, 'health/list_pharmasicst.html', {'pharmacists': pharmacists})

# View to list Junior Health Inspectors
def health_list_junior_health_inspectors(request):
    junior_health_inspectors = JuniorHealthInspectorProfile.objects.filter(fk_healthcare__fk_user=request.user)
    return render(request, 'health/list_jhi.html', {'junior_health_inspectors': junior_health_inspectors})



def user_contact(request):
    return render(request,'patients/contact.html')

# profiles  doctor
from django.utils.dateformat import DateFormat
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateformat import DateFormat
from .models import DoctorProfile


@csrf_exempt
def update_doctor_profile(request):
    if request.method == "POST":
        user = request.user
        doctor = DoctorProfile.objects.get(fk_user=user)

        if 'profile_image' in request.FILES:
            doctor_image, created = DoctImgProfile.objects.get_or_create(fk_user=user)
            doctor_image.profile_image = request.FILES['profile_image']
            doctor_image.save()

        # Get the data from the form (use `.get()` to avoid KeyError if the field is not provided)
        username = request.POST.get("username")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        contact_number = request.POST.get("contact_number")
        medical_registration_number = request.POST.get("medical_registration_number")
        specialization = request.POST.get("specialization")
        qualifications = request.POST.get("qualifications")
        years_of_experience = request.POST.get("years_of_experience")
        address = request.POST.get("address")

        # Update only if the value is provided, otherwise keep existing data
        if username:
            doctor.fk_user.username = username
        if email:
            doctor.fk_user.email = email
        if gender:
            doctor.gender = gender
        if dob:
            doctor.dob = dob
        if contact_number:
            doctor.contact_number = contact_number
        if medical_registration_number:
            doctor.medical_registration_number = medical_registration_number
        if specialization:
            doctor.specialization = specialization
        if qualifications:
            doctor.qualifications = qualifications
        if years_of_experience:
            doctor.years_of_experience = years_of_experience
        if address:
            doctor.address = address

        # Save the changes
        doctor.fk_user.save()  # Save the User model
        doctor.save()  # Save the DoctorProfile model

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def doctors_profile(request):
    user = request.user
    profile_pic = DoctorProfile.objects.filter(fk_user=user)
    scan_profile_pic = DoctImgProfile.objects.filter(fk_user=user).first()
    for doctor in profile_pic:
        if doctor.dob:
            doctor.dob = DateFormat(doctor.dob).format('Y-m-d')
            print(doctor.dob)  # Debugging line to check the value of dob
    return render(request, 'doctor/doctor_profile.html', {'profile_pic': profile_pic,'scan_profile_pic':scan_profile_pic})




def mark_doctor_attendance(request):
    return render(request, 'doctor/mark_attendance.html')


def mark_jhi_attendance(request):
    return render(request, 'jhi/mark_jhi_attendance.html')


def my_jhi_attendance(request):
    user = request.user
    today = date.today()
    year, month = today.year, today.month
    
    # Format today's date as "Day/Month/Year" (e.g., 13/03/2023)
    today_date = today.strftime('%d/%m/%Y')
    
    # Get all attendance records for the user for the current month
    attendance_records = Attendance.objects.filter(user=user, date__year=year, date__month=month)
    attendance_dates = {record.date for record in attendance_records}
    
    # Build calendar structure
    cal = calendar.Calendar(firstweekday=0)  # Start the week on Monday
    month_days = cal.monthdatescalendar(year, month)
    calendar_data = []
    for week in month_days:
        week_data = []
        for day in week:
            if day.month == month:
                status = 'Present' if day in attendance_dates else 'Absent'
                week_data.append({'date': day, 'status': status})
            else:
                week_data.append({'date': None, 'status': None})
        calendar_data.append(week_data)

    return render(request, 'jhi/my_jhi_attendance.html', {
        'calendar': calendar_data,
        'today_date': today_date
    })


import json
import base64
import numpy as np
import face_recognition
from io import BytesIO
from PIL import Image
from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def recognize_face(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            image_data = data.get("image")

            if not image_data:
                return JsonResponse({"success": False, "message": "No image provided"})

            # Decode base64 image
            image_data = image_data.split(",")[1]
            image = Image.open(BytesIO(base64.b64decode(image_data)))

            # Convert image to RGB (Ensures compatibility with face_recognition)
            if image.mode != "RGB":
                image = image.convert("RGB")

            image = np.array(image)  # Convert to numpy array

            # Extract face encodings from the uploaded image
            uploaded_face_encodings = face_recognition.face_encodings(image)

            if not uploaded_face_encodings:
                print("No face detected in uploaded image")
                return JsonResponse({"success": False, "message": "No face detected"})

            uploaded_encoding = uploaded_face_encodings[0]

            # Load stored face encodings
            known_encodings = []
            known_users = []

            doctors = DoctImgProfile.objects.exclude(face_encoding=None)
            nurses = NurseImgProfile.objects.exclude(face_encoding=None)
            asha = AshImgProfile.objects.exclude(face_encoding=None)
            pharmacist = PharmacistImgProfile.objects.exclude(face_encoding=None)
            jhi = JhiImgProfile.objects.exclude(face_encoding=None)


            for doctor in doctors:
                known_encodings.append(np.frombuffer(doctor.face_encoding, dtype=np.float64))
                known_users.append(doctor.fk_user)

            for nurse in nurses:
                known_encodings.append(np.frombuffer(nurse.face_encoding, dtype=np.float64))
                known_users.append(nurse.fk_user)

            for asha in asha:
                known_encodings.append(np.frombuffer(asha.face_encoding, dtype=np.float64))
                known_users.append(asha.fk_user)

            for pharmacist in pharmacist:
                known_encodings.append(np.frombuffer(pharmacist.face_encoding, dtype=np.float64))
                known_users.append(pharmacist.fk_user)

            for jhi in jhi:
                known_encodings.append(np.frombuffer(jhi.face_encoding, dtype=np.float64))
                known_users.append(jhi.fk_user)

            print(f"Loaded {len(known_encodings)} stored face encodings.")

            if not known_encodings:
                return JsonResponse({"success": False, "message": "No stored faces found. Please register first."})

            # Compare faces
            matches = face_recognition.compare_faces(known_encodings, uploaded_encoding, tolerance=0.6)
            face_distances = face_recognition.face_distance(known_encodings, uploaded_encoding)

            if any(matches):
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    user = known_users[best_match_index]  # Get identified user

                    # Check if attendance already exists for today
                    if not Attendance.objects.filter(user=user, date=now().date()).exists():
                        Attendance.objects.create(user=user)
                        print(f"Attendance marked for {user.username}")
                        return JsonResponse({"success": True, "message": f"Attendance marked for {user.username}"})
                    else:
                        print(f"Attendance already exists for {user.username}")
                        return JsonResponse({"success": True, "message": f"Attendance already marked for {user.username}"})

            print("Face not recognized")
            return JsonResponse({"success": False, "message": "Face not recognized"})

        except Exception as e:
            print(f"Error in face recognition: {str(e)}")
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"}, status=500)



from datetime import date, timedelta
import calendar

def my_doctor_attendance(request):
    user = request.user
    today = date.today()
    year, month = today.year, today.month
    
    # Format today's date as "Day/Month/Year" (e.g., 13/03/2023)
    today_date = today.strftime('%d/%m/%Y')
    
    # Get all attendance records for the user for the current month
    attendance_records = Attendance.objects.filter(user=user, date__year=year, date__month=month)
    attendance_dates = {record.date for record in attendance_records}
    
    # Build calendar structure
    cal = calendar.Calendar(firstweekday=0)  # Start the week on Monday
    month_days = cal.monthdatescalendar(year, month)
    calendar_data = []
    for week in month_days:
        week_data = []
        for day in week:
            if day.month == month:
                status = 'Present' if day in attendance_dates else 'Absent'
                week_data.append({'date': day, 'status': status})
            else:
                week_data.append({'date': None, 'status': None})
        calendar_data.append(week_data)

    return render(request, 'doctor/list_attendance.html', {
        'calendar': calendar_data,
        'today_date': today_date
    })


#profile of pharmacist
@csrf_exempt
def update_pharmacist_profile(request):
    
    if request.method == "POST":
        user = request.user
        pharmacist = PharmacistProfile.objects.get(fk_user=user)

        if 'profile_image' in request.FILES:
            pharmacist_image, created = PharmacistImgProfile.objects.get_or_create(fk_user=user)
            pharmacist_image.profile_image = request.FILES['profile_image']
            pharmacist_image.save()

        # Retrieve form data
        username = request.POST.get("username")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        contact_number = request.POST.get("contact_number")
        pharmacy_registration_number = request.POST.get("pharmacy_registration_number")
        qualifications = request.POST.get("qualifications")
        years_of_experience = request.POST.get("years_of_experience")
        address = request.POST.get("address")

        # Update the related user model
        if username:
            user.username = username
        if email:
            user.email = email

        # Update the pharmasict profile fields
        if gender:
            pharmacist.gender = gender
        if dob:
            pharmacist.dob = dob
        if contact_number:
            pharmacist.contact_number = contact_number
        if pharmacy_registration_number:
            pharmacist.pharmacy_registration_number = pharmacy_registration_number
        if qualifications:
            pharmacist.qualifications = qualifications
        if years_of_experience:
            pharmacist.years_of_experience = years_of_experience
        if address:
            pharmacist.address = address

        # Save the updated user and profile objects
        user.save()
        pharmacist.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})



def pharmacist_profile(request):
    user = request.user
    profile_pic = PharmacistProfile.objects.filter(fk_user=user)
    scan_profile_pic = PharmacistImgProfile.objects.filter(fk_user=user).first()
    for pharmacist in profile_pic:
        if pharmacist.dob:
            pharmacist.dob = DateFormat(pharmacist.dob).format('Y-m-d')
            print(pharmacist.dob)  # Debugging line to check the value of dob
    return render(request, 'pharmacist/pharmacist_profile.html', {'profile_pic': profile_pic,'scan_profile_pic':scan_profile_pic})


def mark_pharmacist_attendance(request):
    return render(request, 'pharmacist/mark_pharmacist_attendance.html')
 


import calendar
from datetime import date
from django.shortcuts import render
from .models import Attendance

def my_pharmacist_attendance(request):
    user = request.user
    today = date.today()
    year, month = today.year, today.month
    
    # Format today's date as "Day/Month/Year" (e.g., 13/03/2023)
    today_date = today.strftime('%d/%m/%Y')
    
    # Get all attendance records for the user for the current month
    attendance_records = Attendance.objects.filter(user=user, date__year=year, date__month=month)
    attendance_dates = {record.date for record in attendance_records}
    
    # Build calendar structure
    cal = calendar.Calendar(firstweekday=0)  # Start the week on Monday
    month_days = cal.monthdatescalendar(year, month)
    calendar_data = []
    for week in month_days:
        week_data = []
        for day in week:
            if day.month == month:
                status = 'Present' if day in attendance_dates else 'Absent'
                week_data.append({'date': day, 'status': status})
            else:
                week_data.append({'date': None, 'status': None})
        calendar_data.append(week_data)

    return render(request, 'pharmacist/my_pharmacist_attendance.html', {
        'calendar': calendar_data,
        'today_date': today_date
    })


# Profile Of PHN

@csrf_exempt
def update_phn_profile(request):
    
    if request.method == "POST":
        user = request.user
        phn = PublicHealthNurseProfile.objects.get(fk_user=user)

        if 'profile_image' in request.FILES:
            phn_image, created = NurseImgProfile.objects.get_or_create(fk_user=user)
            phn_image.profile_image = request.FILES['profile_image']
            phn_image.save()

        # Retrieve form data
        username = request.POST.get("username")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        contact_number = request.POST.get("contact_number")
        nursing_license_number = request.POST.get("nursing_license_number")
        qualifications = request.POST.get("qualifications")
        years_of_experience = request.POST.get("years_of_experience")
        training_in_public_health = request.POST.get("training_in_public_health")
        address = request.POST.get("address")

        # Update the related user model
        if username:
            user.username = username
        if email:
            user.email = email

        # Update the Public Health Nurse profile fields
        if gender:
            phn.gender = gender
        if dob:
            phn.dob = dob
        if contact_number:
            phn.contact_number = contact_number
        if nursing_license_number:
            phn.nursing_license_number = nursing_license_number
        if qualifications:
            phn.qualifications = qualifications
        if years_of_experience:
            phn.years_of_experience = years_of_experience
        if training_in_public_health:
            phn.training_in_public_health = training_in_public_health
        if address:
            phn.address = address

        # Save the updated user and profile objects
        user.save()
        phn.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})



def phn_profile(request):
    user = request.user
    profile_pic = PublicHealthNurseProfile.objects.filter(fk_user=user)
    scan_profile_pic = NurseImgProfile.objects.filter(fk_user=user).first()
    for phn in profile_pic:
        if phn.dob:
            phn.dob = DateFormat(phn.dob).format('Y-m-d')
            print(phn.dob)  # Debugging line to check the value of dob
    return render(request, 'phn/phn_profile.html', {'profile_pic': profile_pic,'scan_profile_pic':scan_profile_pic})


def mark_phn_attendance(request):
    return render(request, 'phn/mark_phn_attendance.html')


import calendar
from datetime import date
from django.shortcuts import render
from .models import Attendance

def my_phn_attendance(request):
    user = request.user
    today = date.today()
    year, month = today.year, today.month
    
    # Format today's date as "Day/Month/Year" (e.g., 13/03/2023)
    today_date = today.strftime('%d/%m/%Y')
    
    # Get all attendance records for the user for the current month
    attendance_records = Attendance.objects.filter(user=user, date__year=year, date__month=month)
    attendance_dates = {record.date for record in attendance_records}
    
    # Build calendar structure
    cal = calendar.Calendar(firstweekday=0)  # Start the week on Monday
    month_days = cal.monthdatescalendar(year, month)
    calendar_data = []
    for week in month_days:
        week_data = []
        for day in week:
            if day.month == month:
                status = 'Present' if day in attendance_dates else 'Absent'
                week_data.append({'date': day, 'status': status})
            else:
                week_data.append({'date': None, 'status': None})
        calendar_data.append(week_data)

    return render(request, 'phn/my_phn_attendance.html', {
        'calendar': calendar_data,
        'today_date': today_date
    })

# Profile Of ASHA

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ASHAWorkerProfile, AshImgProfile

@csrf_exempt
def update_asha_profile(request):
    if request.method == "POST":
        user = request.user
        # Retrieve the ASHAWorkerProfile associated with this user
        try:
            asha_profile = ASHAWorkerProfile.objects.get(fk_user=user)
        except ASHAWorkerProfile.DoesNotExist:
            return JsonResponse({"success": False, "message": "ASHA Worker profile not found."})

        # Update the profile image if provided in the form
        if 'profile_image' in request.FILES:
            asha_image, created = AshImgProfile.objects.get_or_create(fk_user=user)
            asha_image.profile_image = request.FILES['profile_image']
            asha_image.save()

        # Retrieve form data (ensure your form field names match these)
        username = request.POST.get("username")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        contact_number = request.POST.get("contact_number")
        asha_worker_id = request.POST.get("asha_worker_id")
        community_assigned = request.POST.get("community_assigned")
        training_details = request.POST.get("training_details")
        experience_in_health_awareness = request.POST.get("experience_in_health_awareness")
        address = request.POST.get("address")

        # Update the related CustomUser fields if provided
        if username:
            user.username = username
        if email:
            user.email = email

        # Update all fields in the ASHAWorkerProfile model
        if gender:
            asha_profile.gender = gender
        if dob:
            asha_profile.dob = dob
        if contact_number:
            asha_profile.contact_number = contact_number
        if asha_worker_id:
            asha_profile.asha_worker_id = asha_worker_id
        if community_assigned:
            asha_profile.community_assigned = community_assigned
        if training_details:
            asha_profile.training_details = training_details
        if experience_in_health_awareness:
            asha_profile.experience_in_health_awareness = experience_in_health_awareness
        if address:
            asha_profile.address = address

        # Save changes to both the user and the ASHAWorkerProfile
        user.save()
        asha_profile.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})



def asha_profile(request):
    user = request.user
    profile_pic = ASHAWorkerProfile.objects.filter(fk_user=user)
    scan_profile_pic = AshImgProfile.objects.filter(fk_user=user).first()
    for phn in profile_pic:
        if phn.dob:
            phn.dob = DateFormat(phn.dob).format('Y-m-d')
            print(phn.dob)  # Debugging line to check the value of dob
    return render(request, 'asha/asha_profile.html', {'profile_pic': profile_pic,'scan_profile_pic':scan_profile_pic})



def mark_asha_attendance(request):
    return render(request, 'asha/mark_asha_attendance.html')


import calendar
from datetime import date
from django.shortcuts import render
from .models import Attendance

def my_asha_attendance(request):
    user = request.user
    today = date.today()
    year, month = today.year, today.month
    
    # Format today's date as "Day/Month/Year" (e.g., 13/03/2023)
    today_date = today.strftime('%d/%m/%Y')
    
    # Get all attendance records for the user for the current month
    attendance_records = Attendance.objects.filter(user=user, date__year=year, date__month=month)
    attendance_dates = {record.date for record in attendance_records}
    
    # Build calendar structure
    cal = calendar.Calendar(firstweekday=0)  # Start the week on Monday
    month_days = cal.monthdatescalendar(year, month)
    calendar_data = []
    for week in month_days:
        week_data = []
        for day in week:
            if day.month == month:
                status = 'Present' if day in attendance_dates else 'Absent'
                week_data.append({'date': day, 'status': status})
            else:
                week_data.append({'date': None, 'status': None})
        calendar_data.append(week_data)

    return render(request, 'asha/my_asha_attendance.html', {
        'calendar': calendar_data,
        'today_date': today_date
    })



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserMessage

def user_message_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if not name or not email or not phone or not message:
            messages.error(request, "All fields are required!")
            return redirect('landing_page')

        UserMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect('landing_page')

    return render(request, "dashboard/landing.html")

def user_message_list(request):
    messages = UserMessage.objects.all() 
    return render(request,'admin/contact_list.html',{'messages': messages})


def user_message_delete(req,id):
    a =UserMessage.objects.get(id=id)
    a.delete()
    return redirect('user_message_list')

from django.shortcuts import render
from .models import Attendance

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from .models import Attendance

def doct_list_all_att(request):
    query = request.GET.get('q', '').strip()
    attendance = Attendance.objects.exclude(user__role=5)

    # Mapping role names to their integer values
    role_mapping = {name.lower(): value for value, name in ROLE_CHOICES}
    role_value = role_mapping.get(query.lower())

    # Combined search for username, email, or role
    if query:
        attendance = attendance.filter(
            Q(user__username__icontains=query) | 
            Q(user__email__icontains=query) | 
            (Q(user__role=role_value) if role_value is not None else Q())
        )

    paginator = Paginator(attendance, 10)  # 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    present_dates = ", ".join(
        date.strftime('%Y-%m-%d') for date in set(attendance.values_list('date', flat=True))
    )

    return render(request, 'doctor/list_all.html', {
        'attendance': page_obj,
        'present_dates': present_dates,
        'query': query
    })



def phn_list_all_att(request):
    query = request.GET.get('q', '').strip()
    attendance = Attendance.objects.filter(user__role=5)  # Only ASHA Workers

    # Search by username or email (no role search)
    if query:
        attendance = attendance.filter(
            Q(user__username__icontains=query) | 
            Q(user__email__icontains=query)
        )

    paginator = Paginator(attendance, 10)  # 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    present_dates = ", ".join(
        date.strftime('%Y-%m-%d') for date in set(attendance.values_list('date', flat=True))
    )

    return render(request, 'phn/list_all.html', {
        'attendance': page_obj,
        'present_dates': present_dates,
        'query': query
    })

##################################################################################################################
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import JuniorHealthInspectorProfile, JhiImgProfile


def jhi_profile(request):
    user = request.user
    profile_pic = JuniorHealthInspectorProfile.objects.filter(fk_user=user)
    scan_profile_pic = JhiImgProfile.objects.filter(fk_user=user).first()
    for phn in profile_pic:
        if phn.dob:
            phn.dob = DateFormat(phn.dob).format('Y-m-d')
            print(phn.dob)  # Debugging line to check the value of dob
    return render(request, 'jhi/jhi_profile.html', {'profile_pic': profile_pic,'scan_profile_pic':scan_profile_pic})


@csrf_exempt
def update_jhi_profile(request):
    if request.method == "POST":
        user = request.user
        
        jhi = JuniorHealthInspectorProfile.objects.get(fk_user=user)

        if 'profile_image' in request.FILES:
            jhi_image, created = JhiImgProfile.objects.get_or_create(fk_user=user)
            jhi_image.profile_image = request.FILES['profile_image']
            jhi_image.save()

        username = request.POST.get("username")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        contact_number = request.POST.get("contact_number")
        inspection_license_number = request.POST.get("inspection_license_number")
        qualifications = request.POST.get("qualifications")
        experience_in_health_inspection = request.POST.get("experience_in_health_inspection")
        address = request.POST.get("address")

        if username:
            user.username = username
        if email:
            user.email = email

        if gender:
            jhi.gender = gender
        if dob:
            jhi.dob = dob
        if contact_number:
            jhi.contact_number = contact_number
        if inspection_license_number:
            jhi.inspection_license_number = inspection_license_number
        if qualifications:
            jhi.qualifications = qualifications
        if experience_in_health_inspection:
            jhi.experience_in_health_inspection = experience_in_health_inspection
        if address:
            jhi.address = address

        user.save()
        jhi.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


###########################################################################################

from django.shortcuts import render
from .models import DoctorProfile

from django.shortcuts import render
from .models import HealthCareProfile, DoctorProfile

from django.utils.timezone import now
from .models import DoctorProfile, HealthCareProfile, Attendance

def find_my_doctor(request):
    health_center_id = request.GET.get('health_center_id')
    query = request.GET.get('q', '')
    today = now().date()

    health_centers = HealthCareProfile.objects.all()
    doctors = DoctorProfile.objects.filter(fk_healthcare=health_center_id) if health_center_id else DoctorProfile.objects.all()
    patient_profile = PatientProfile.objects.get(fk_user=request.user)


    if query:
        doctors = doctors.filter(fk_user__username__icontains=query)

    # Check attendance for each doctor
    for doctor in doctors:
        doctor.is_present = Attendance.objects.filter(user=doctor.fk_user, date=today).exists()

    return render(request, 'patients/find_my_doctor.html', {
        'health_centers': health_centers,
        'doctors': doctors,
        'query': query,
        'selected_health_center': health_center_id,
        'patient_profile':patient_profile,
    })


###################################################################################################################
#Asha worker details added

from django.utils.dateparse import parse_date
from datetime import datetime
from .models import *

def asha_worker_list(request):
    # Fetch all data from the models
    households = Household.objects.all()
    family_members = FamilyMember.objects.all()
    chronic_illnesses = ChronicIllness.objects.all()
    follow_up_patients = FollowUpPatient.objects.all()
    sanitation_hygiene = SanitationHygiene.objects.all()
    child_health = ChildHealth.objects.all()
    visit_details = VisitDetails.objects.all()
    pregnant_women = PregnantWoman.objects.all()
    emergency_referrals = EmergencyReferral.objects.all()
    health_education = HealthEducation.objects.all()

    # Pass the data to the template
    context = {
        'households': households,
        'family_members': family_members,
        'chronic_illnesses': chronic_illnesses,
        'follow_up_patients': follow_up_patients,
        'sanitation_hygiene': sanitation_hygiene,
        'child_health': child_health,
        'visit_details': visit_details,
        'pregnant_women': pregnant_women,
        'emergency_referrals': emergency_referrals,
        'health_education': health_education,
    }

    return render(request, 'asha/asha_worker_list.html', context)



def save_household_data(request):
    user=request.user
    if request.method == "POST":
        # Create Household record
        head_of_household = request.POST.get("head_of_household")
        contact_number = request.POST.get("contact_number")
        address = request.POST.get("address")
        household = Household.objects.create(
            fk_user=user,
            head_of_household=head_of_household,
            contact_number=contact_number,
            address=address
        )

        # Create FamilyMember records and store them using lower-cased names for lookup
        member_names = request.POST.getlist("member_name[]")
        member_ages = request.POST.getlist("member_age[]")
        member_genders = request.POST.getlist("member_gender[]")
        member_occupations = request.POST.getlist("member_occupation[]")
        
        family_members = {}
        for name, age, gender, occupation in zip(member_names, member_ages, member_genders, member_occupations):
            fm = FamilyMember.objects.create(
                household=household,
                name=name,
                age=int(age),
                gender=gender,
                occupation=occupation if occupation else None
            )
            # Store with lower-case key for lookup
            family_members[name.strip().lower()] = fm

        # Create ChronicIllness records for each chronic illness entry
    chronic_family_member_names = request.POST.getlist("chronic_family_member[]")
    chronic_illnesses = request.POST.getlist("chronic_illness[]")
    medications_prescribed_list = request.POST.getlist("medications_prescribed[]")
    following_medications_list = request.POST.getlist("following_medication[]")

    for i, (name, illness, medications) in enumerate(zip(chronic_family_member_names, chronic_illnesses, medications_prescribed_list)):
        fm = family_members.get(name.strip().lower())
        if fm:
            # Check if the following_medication checkbox was ticked for this record.
            # Since the checkbox is only included if checked, we assume it's True if the length of the list is greater than the current index.
            following = (i < len(following_medications_list) and following_medications_list[i].lower() == "true")
            ChronicIllness.objects.create(
                family_member=fm,
                illness=illness,
                medications_prescribed=medications,
                following_medication=following
            )


        # Create FollowUpPatient records for each follow-up entry.
        # Make sure the form field for the follow-up family member is named appropriately.
        followup_family_member_names = request.POST.getlist("followup_family_member[]")
        followup_diagnoses = request.POST.getlist("followup_diagnosis[]")
        last_checkup_dates = request.POST.getlist("last_checkup_date[]")
        next_followup_dates = request.POST.getlist("next_followup_date[]")
        for name, diagnosis, last_date, next_date in zip(followup_family_member_names, followup_diagnoses, last_checkup_dates, next_followup_dates):
            fm = family_members.get(name.strip().lower())
            if fm:
                FollowUpPatient.objects.create(
                    family_member=fm,
                    diagnosis=diagnosis,
                    last_checkup_date=parse_date(last_date) if last_date else None,
                    next_followup_date=parse_date(next_date) if next_date else None
                )

        # Create SanitationHygiene record
        has_toilet = request.POST.get("has_toilet") == "true"
        has_clean_drinking_water = request.POST.get("has_clean_drinking_water") == "true"
        has_handwashing_facility = request.POST.get("has_handwashing_facility") == "true"

        SanitationHygiene.objects.create(
            household=household,
            has_toilet=has_toilet,
            has_clean_drinking_water=has_clean_drinking_water,
            has_handwashing_facility=has_handwashing_facility
        )

       # Save Children Data
        child_names = request.POST.getlist('child_name[]')
        child_ages = request.POST.getlist('child_age[]')
        child_weights = request.POST.getlist('child_weight[]')
        immunization_statuses = request.POST.getlist('immunization_status[]')
        nutritional_statuses = request.POST.getlist('nutritional_status[]')
        vaccination_due_dates = request.POST.getlist('vaccination_due_date[]')

        for i in range(len(child_names)):
            # Fetch the vaccination_done value for this child
            vaccination_done = request.POST.get(f'vaccination_done_{i}') == "yes"

            # Skip if all fields are empty
            if (
                not child_names[i].strip() and
                not child_ages[i].strip() and
                not child_weights[i].strip() and
                not immunization_statuses[i].strip() and
                not nutritional_statuses[i].strip() and
                not vaccination_due_dates[i].strip()
            ):
                continue
            
            ChildHealth.objects.create(
                family_member=household,  # Assign the Household instance
                child_name=child_names[i].strip() if child_names[i].strip() else None,
                child_age=int(child_ages[i]) if child_ages[i].strip() else None,
                birth_weight=float(child_weights[i]) if child_weights[i].strip() else None,
                immunization_status=immunization_statuses[i].strip() if immunization_statuses[i].strip() else None,
                nutritional_status=nutritional_statuses[i].strip() if nutritional_statuses[i].strip() else None,
                vaccination_done=vaccination_done,
                vaccination_due_date=parse_date(vaccination_due_dates[i]) if vaccination_due_dates[i].strip() else None
            )

         # Save Visit Details

         
# Save Visit Details
        visit_dates = request.POST.getlist("visit_date[]")
        visit_reasons = request.POST.getlist("visit_reason[]")
        visit_symptoms = request.POST.getlist("visit_symptoms[]")

        for date, reason, symptoms in zip(visit_dates, visit_reasons, visit_symptoms):
            if date:  # Ensure date is not empty
                VisitDetails.objects.create(
                    household=household,
                    date_time=datetime.strptime(date, "%Y-%m-%dT%H:%M"),  # Convert input format
                    reason_for_visit=reason,
                    symptoms_reported=symptoms
                )

            


        # Save Pregnant Women Data
        pregnant_members = request.POST.getlist("pregnant_member[]")
        expected_delivery_dates = request.POST.getlist("expected_delivery_date[]")
        antenatal_checkups = request.POST.getlist("antenatal_checkups[]")

        print("Pregnant Members:", pregnant_members)
        print("Expected Delivery Dates:", expected_delivery_dates)
        print("Antenatal Checkups:", antenatal_checkups)

        for name, delivery_date, checkup in zip(pregnant_members, expected_delivery_dates, antenatal_checkups):
            print(f"Processing: Name={name}, Delivery Date={delivery_date}, Checkup={checkup}")
            
            if not name.strip() and not delivery_date.strip():
                continue

            PregnantWoman.objects.create(
                household=household,  # Ensure household is correctly defined
                name=name if name.strip() else None,  # Save as None if empty
                expected_delivery_date=parse_date(delivery_date) if delivery_date.strip() else None,  # Save as None if empty
                antenatal_checkups_completed=(checkup == "true")  # Use correct field name
            )
            print(f"Saved: {name}")


        # Save Emergency Referral Data
        EmergencyReferral.objects.create(
            household=household,
            critical_health_issue=request.POST.get("emergency_issue") == "true",
            referred_to_health_center=request.POST.get("referred_to_center") == "true",
            referral_details=request.POST.get("referral_details", "")  # Default empty string if no input
        )


        # Save Health Education Data
        HealthEducation.objects.create(
            visit=household,
            nutrition=request.POST.get("nutrition") == "true",
            breastfeeding=request.POST.get("breastfeeding") == "true",
            family_planning=request.POST.get("family_planning") == "true",
            sanitation_hygiene=request.POST.get("sanitation_hygiene") == "true"
        )

        return redirect("save_household")
 
        

    return render(request, "asha/asha_worker_form.html")


    #####################################################################################################

def add_survey(request):
    user=request.user
    households = Household.objects.all()

    if request.method == "POST":
        # Collect data from the form
        household_id = request.POST.get("household")
        
        # Helper function to safely convert form input to integer
        def get_int_value(key):
            value = request.POST.get(key, "0")  # Default to "0" if key is missing or empty
            return int(value) if value.strip() else 0  # Convert to int if not empty, else return 0

        # Fever Cases
        fever_7_days_or_more_male_5_or_less = get_int_value("fever_7_days_or_more_male_5_or_less")
        fever_7_days_or_more_male_above_5 = get_int_value("fever_7_days_or_more_male_above_5")
        fever_7_days_or_more_female_5_or_less = get_int_value("fever_7_days_or_more_female_5_or_less")
        fever_7_days_or_more_female_above_5 = get_int_value("fever_7_days_or_more_female_above_5")
        fever_less_than_7_days_male_5_or_less = get_int_value("fever_less_than_7_days_male_5_or_less")
        fever_less_than_7_days_male_above_5 = get_int_value("fever_less_than_7_days_male_above_5")
        fever_less_than_7_days_female_5_or_less = get_int_value("fever_less_than_7_days_female_5_or_less")
        fever_less_than_7_days_female_above_5 = get_int_value("fever_less_than_7_days_female_above_5")
        fever_with_rash = get_int_value("fever_with_rash")
        fever_with_bleeding = get_int_value("fever_with_bleeding")
        fever_with_altered_sensorium = get_int_value("fever_with_altered_sensorium")

        # Cough Cases
        cough_2_weeks_or_less_with_fever = get_int_value("cough_2_weeks_or_less_with_fever")
        cough_2_weeks_or_less_without_fever = get_int_value("cough_2_weeks_or_less_without_fever")
        cough_more_than_2_weeks_with_fever = get_int_value("cough_more_than_2_weeks_with_fever")
        cough_more_than_2_weeks_without_fever = get_int_value("cough_more_than_2_weeks_without_fever")

        # Diarrhea Cases
        loose_watery_stools_with_blood_less_than_2_weeks = get_int_value("loose_watery_stools_with_blood_less_than_2_weeks")
        loose_watery_stools_without_blood_less_than_2_weeks = get_int_value("loose_watery_stools_without_blood_less_than_2_weeks")

        # Other Diseases
        jaundice_less_than_4_weeks = get_int_value("jaundice_less_than_4_weeks")
        acute_flaccid_paralysis = get_int_value("acute_flaccid_paralysis")

        # Malaria Cases
        malaria_vivax_rdt = get_int_value("malaria_vivax_rdt")
        malaria_falciparum_rdt = get_int_value("malaria_falciparum_rdt")
        malaria_mixed_rdt = get_int_value("malaria_mixed_rdt")

        # Animal Bites
        animal_bite_snake = get_int_value("animal_bite_snake")
        animal_bite_dog = get_int_value("animal_bite_dog")
        animal_bite_other = get_int_value("animal_bite_other")

        # Leptospirosis
        leptospirosis_rdt = get_int_value("leptospirosis_rdt")

        # Summary Fields
        total_deaths = get_int_value("total_deaths")

        # Get the Household instance
        household = Household.objects.get(id=household_id)

        # Create and save the HealthSurvey instance
        survey = HealthSurvey(
            fk_user=user,
            household=household,
            fever_7_days_or_more_male_5_or_less=fever_7_days_or_more_male_5_or_less,
            fever_7_days_or_more_male_above_5=fever_7_days_or_more_male_above_5,
            fever_7_days_or_more_female_5_or_less=fever_7_days_or_more_female_5_or_less,
            fever_7_days_or_more_female_above_5=fever_7_days_or_more_female_above_5,
            fever_less_than_7_days_male_5_or_less=fever_less_than_7_days_male_5_or_less,
            fever_less_than_7_days_male_above_5=fever_less_than_7_days_male_above_5,
            fever_less_than_7_days_female_5_or_less=fever_less_than_7_days_female_5_or_less,
            fever_less_than_7_days_female_above_5=fever_less_than_7_days_female_above_5,
            fever_with_rash=fever_with_rash,
            fever_with_bleeding=fever_with_bleeding,
            fever_with_altered_sensorium=fever_with_altered_sensorium,
            cough_2_weeks_or_less_with_fever=cough_2_weeks_or_less_with_fever,
            cough_2_weeks_or_less_without_fever=cough_2_weeks_or_less_without_fever,
            cough_more_than_2_weeks_with_fever=cough_more_than_2_weeks_with_fever,
            cough_more_than_2_weeks_without_fever=cough_more_than_2_weeks_without_fever,
            loose_watery_stools_with_blood_less_than_2_weeks=loose_watery_stools_with_blood_less_than_2_weeks,
            loose_watery_stools_without_blood_less_than_2_weeks=loose_watery_stools_without_blood_less_than_2_weeks,
            jaundice_less_than_4_weeks=jaundice_less_than_4_weeks,
            acute_flaccid_paralysis=acute_flaccid_paralysis,
            malaria_vivax_rdt=malaria_vivax_rdt,
            malaria_falciparum_rdt=malaria_falciparum_rdt,
            malaria_mixed_rdt=malaria_mixed_rdt,
            animal_bite_snake=animal_bite_snake,
            animal_bite_dog=animal_bite_dog,
            animal_bite_other=animal_bite_other,
            leptospirosis_rdt=leptospirosis_rdt,
            total_deaths=total_deaths,
        )
        survey.save()

        return redirect("survey_list")  # Redirect to a success page or another view

    return render(request, "asha/add_survey.html", {
        "households": households,
    })

from django.shortcuts import render
from .models import HealthSurvey

def survey_list(request):
    # Fetch all HealthSurvey objects from the database
    surveys = HealthSurvey.objects.all()
    
    # Pass the surveys to the template
    return render(request, "asha/survey_list.html", {
        "surveys": surveys,
    })




########################################################################################################################


def phn_pregenent_list(request):
    pregnant_women = PregnantWoman.objects.all()
    maternal_cases = MaternalCase.objects.all()
    return render(request, 'phn/phn_pregenent_list.html',
                  {'pregnant_women':pregnant_women,
                   'maternal_cases':maternal_cases})

from django.db import models
from django.shortcuts import render, redirect



# Views
def phn_pregenent_add(request):
    if request.method == 'POST':
        maternal_case = MaternalCase(
            household_name=request.POST.get('household'),
            pregnant_member_name=request.POST.get('pregnant_member'),
            antenatal_checkups=request.POST.get('antenatal_checkups') == 'true',
            full_name=request.POST.get('full_name'),
            age=request.POST.get('age'),
            contact_number=request.POST.get('contact_number'),
            husband_name=request.POST.get('husband_name'),
            husband_contact_number=request.POST.get('husband_contact_number'),
            address=request.POST.get('address'),
            last_menstrual_period=datetime.strptime(request.POST.get('last_menstrual_period'), '%Y-%m-%d').date() if request.POST.get('last_menstrual_period') else None,
            gestational_age_weeks=request.POST.get('gestational_age'),
            pregnancy_risk_factor=request.POST.get('pregnancy_risk_factor'),
            number_of_pregnancies=request.POST.get('number_of_pregnancies'),
            number_of_live_births=request.POST.get('number_of_live_births')
        )
        maternal_case.save()
        return redirect('phn_pregenent_list')
    
    return render(request, 'phn/phn_pregenent_add.html')

#####################################################################################


def maternal_visit_list(request):
    visit_schedules = MaternalVisitSchedule.objects.all()
    return render(request, 'phn/maternal_visit_list.html', {'visit_schedules': visit_schedules})


def maternal_visit_add(request): 
    maternal_cases = MaternalCase.objects.all()
    visit_types = MaternalVisitSchedule.VISIT_TYPES
    visit_statuses = MaternalVisitSchedule.VISIT_STATUSES

    if request.method == 'POST':
        maternal_case_id = request.POST.get('maternal_case')
        visit_date = request.POST.get('visit_date')
        follow_up_date = request.POST.get('follow_up_date')
        visit_type = request.POST.get('visit_type')
        visit_status = request.POST.get('visit_status')

        maternal_case = MaternalCase.objects.get(id=maternal_case_id)

        MaternalVisitSchedule.objects.create(
            maternal_case=maternal_case,
            visit_date=datetime.strptime(visit_date, '%Y-%m-%d').date() if visit_date else None,
            follow_up_date=datetime.strptime(follow_up_date, '%Y-%m-%d').date() if follow_up_date else None,
            visit_type=visit_type,
            visit_status=visit_status
        )
        return redirect('maternal_visit_list')
    
    return render(request, 'phn/maternal_visit_add.html', {'maternal_cases': maternal_cases, 'visit_types': visit_types, 'visit_statuses': visit_statuses})



#######################################################################################################

from django.shortcuts import render, redirect
from .models import ChildGrowthRecord



def child_growth_list(request):
    records = ChildGrowthRecord.objects.all()
    return render(request, 'asha/child_growth_list.html', {'records': records})

def add_child_growth_record(request):
    user=request.user
    GENDER_CHOICES = ChildGrowthRecord.GENDER_CHOICES
    IMMUNIZATION_STATUS_CHOICES = ChildGrowthRecord.IMMUNIZATION_STATUS_CHOICES
    YES_NO_CHOICES = ChildGrowthRecord.YES_NO_CHOICES


    if request.method == 'POST':
        ChildGrowthRecord.objects.create(
            fk_user=user,
            child_name=request.POST['child_name'],
            date_of_birth=request.POST['date_of_birth'],
            gender=request.POST['gender'],
            guardian_name=request.POST['guardian_name'],
            contact_number=request.POST['contact_number'],
            weight=request.POST['weight'],
            height=request.POST['height'],
            head_circumference=request.POST['head_circumference'],
            mid_upper_arm_circumference=request.POST['mid_upper_arm_circumference'],
            exclusive_breastfeeding_till_6_months=request.POST['exclusive_breastfeeding_till_6_months'],
            complementary_feeding_started=request.POST['complementary_feeding_started'],
            vitamin_a_supplementation=request.POST['vitamin_a_supplementation'],
            immunization_status=request.POST['immunization_status']
        )
        return redirect('child_growth_list')

    return render(request, 'asha/add_child_growth_record.html', {
        'GENDER_CHOICES': GENDER_CHOICES,
        'IMMUNIZATION_STATUS_CHOICES': IMMUNIZATION_STATUS_CHOICES,
        'YES_NO_CHOICES': YES_NO_CHOICES
    })



from django.shortcuts import render, get_object_or_404, redirect
from .models import ChildGrowthRecord

def update_child_growth_record(request, id):
    record = get_object_or_404(ChildGrowthRecord, id=id)

    GENDER_CHOICES = ChildGrowthRecord.GENDER_CHOICES
    IMMUNIZATION_STATUS_CHOICES = ChildGrowthRecord.IMMUNIZATION_STATUS_CHOICES
    YES_NO_CHOICES = ChildGrowthRecord.YES_NO_CHOICES

    if request.method == 'POST':
        record.child_name = request.POST['child_name']
        record.date_of_birth = request.POST['date_of_birth']
        record.gender = request.POST['gender']
        record.guardian_name = request.POST['guardian_name']
        record.contact_number = request.POST['contact_number']
        record.weight = request.POST['weight']
        record.height = request.POST['height']
        record.head_circumference = request.POST['head_circumference']
        record.mid_upper_arm_circumference = request.POST['mid_upper_arm_circumference']
        record.exclusive_breastfeeding_till_6_months = request.POST['exclusive_breastfeeding_till_6_months']
        record.complementary_feeding_started = request.POST['complementary_feeding_started']
        record.vitamin_a_supplementation = request.POST['vitamin_a_supplementation']
        record.immunization_status = request.POST['immunization_status']

        record.save()
        return redirect('child_growth_list')

    return render(request, 'asha/update_child_growth_record.html', {
        'record': record,
        'GENDER_CHOICES': GENDER_CHOICES,
        'IMMUNIZATION_STATUS_CHOICES': IMMUNIZATION_STATUS_CHOICES,
        'YES_NO_CHOICES': YES_NO_CHOICES
    })



######################################################################################################################

from django.shortcuts import render, redirect
from .models import VaccinationRecord

def register_vaccination(request):
    vaccinator = request.user
    if request.method == "POST":
        patient_name = request.POST.get('patient_name')
        age = request.POST.get('age')
        contact_number = request.POST.get('contact_number')
        location = request.POST.get('location')
        address = request.POST.get('address')
        vaccine_name = request.POST.get('vaccine_name')
        vaccination_date = request.POST.get('vaccination_date')
        route_of_administration = request.POST.get('route_of_administration')

        VaccinationRecord.objects.create(
            vaccinator_name=vaccinator,
            patient_name=patient_name,
            age=age,
            contact_number=contact_number,
            location=location,
            address=address,
            vaccine_name=vaccine_name,
            vaccination_date=vaccination_date,
            route_of_administration=route_of_administration
        )
        return redirect('register_vaccination_list')

    vaccine_choices = VaccinationRecord.VACCINE_CHOICES
    route_choices = VaccinationRecord.ROUTE_CHOICES
    return render(request, 'jhi/register_vaccination.html', {'vaccine_choices': vaccine_choices, 'route_choices': route_choices})


def register_vaccination_list(request):
    records = VaccinationRecord.objects.all()
    return render(request, 'jhi/register_vaccination_list.html', {'records': records})


##########################################################################################################


def vaccination_list(request):
    schedules = VaccinationSchedule.objects.all()
    return render(request, 'phn/vaccination_list.html', {'schedules': schedules})

# Create view
def vaccination_create(request):  
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        age_group = request.POST.get('age_group')
        vaccines = request.POST.get('vaccines')
        vaccination_date = request.POST.get('vaccination_date')

        VaccinationSchedule.objects.create(
            vaccinator_name=request.user,
            full_name=full_name,
            date_of_birth=date_of_birth,
            gender=gender,
            age_group=age_group,
            vaccines=vaccines,
            vaccination_date=vaccination_date
        )
        return redirect('vaccination_list')
    age_choices = VaccinationSchedule.AGE_CHOICES
    GENDER_CHOICES = VaccinationSchedule.gender_choices
    return render(request, 'phn/vaccination_form.html', {'age_choices': age_choices, 'gender_choices': GENDER_CHOICES,})


def vaccination_delete(request,id):
    a=VaccinationSchedule.objects.get(id=id)
    a.delete()
    return redirect('vaccination_list')


###################################################################################################################
from django.shortcuts import render, redirect
from .models import Bedridden

def add_bedridden(request):
    # Ensure we're using the correct model attributes
    gender_choices = Bedridden.GENDER_CHOICES
    dependency_choices = Bedridden.DEPENDENCY_CHOICES

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        existing_conditions = request.POST.get('existing_conditions')
        current_medications = request.POST.get('current_medications')
        allergies = request.POST.get('allergies')
        past_surgeries = request.POST.get('past_surgeries')
        duration_of_bedridden = request.POST.get('duration_of_bedridden')
        primary_diagnosis = request.POST.get('primary_diagnosis')
        level_of_dependency = request.POST.get('level_of_dependency')
        caregiver_name = request.POST.get('caregiver_name')
        caregiver_contact = request.POST.get('caregiver_contact')

        # Ensure date field is correctly formatted or left blank
        dob = dob if dob else None
        age = int(age) if age else None

        Bedridden.objects.create(
            fk_user=request.user,
            full_name=full_name,
            dob=dob,
            age=age,
            gender=gender,
            contact_number=contact_number,
            address=address,
            existing_conditions=existing_conditions,
            current_medications=current_medications,
            allergies=allergies,
            past_surgeries=past_surgeries,
            duration_of_bedridden=duration_of_bedridden,
            primary_diagnosis=primary_diagnosis,
            level_of_dependency=level_of_dependency,
            caregiver_name=caregiver_name,
            caregiver_contact=caregiver_contact
        )
        return redirect('list_bedridden')

    return render(request, 'phn/add_bedridden.html', {
        'gender_choices': gender_choices,
        'dependency_choices': dependency_choices
    })






def list_bedridden(request):
    data=Bedridden.objects.all()
    return render(request,'phn/list_bedridden.html',{'data':data})



########################################################

from django.shortcuts import render, redirect
from .models import *

def schedule_bedridden_visit(request):
    health_worker_choices = BedriddenVisit.HEALTH_WORKER_CHOICES
    patients = Bedridden.objects.all()
    asha_workers = ASHAWorkerProfile.objects.all()

    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        scheduled_date = request.POST.get('scheduled_date')
        visit_time = request.POST.get('visit_time')
        health_worker = request.POST.get('health_worker')
        asha_worker_id = request.POST.get('asha_worker')
        follow_up = request.POST.get('follow_up') == 'on'

        patient = Bedridden.objects.get(id=patient_id)
        asha_worker = ASHAWorkerProfile.objects.get(id=asha_worker_id)

        BedriddenVisit.objects.create(
            fk_user=request.user,
            patient=patient,
            scheduled_date=scheduled_date,
            visit_time=visit_time,
            assigned_health_worker=health_worker,
            assigned_asha_worker=asha_worker,
            follow_up_required=follow_up
        )
        return redirect('schedule_bedridden_visit_list')

    return render(request, 'phn/schedule_bedridden_visit.html', {
        'health_worker_choices': health_worker_choices,
        'patients': patients,
        'asha_workers': asha_workers
    })


def schedule_bedridden_visit_list(request):
    data=BedriddenVisit.objects.all()
    return render(request,'phn/schedule_bedridden_visit_list.html',{'data':data})



##########################################################################################3

#medicine

from django.shortcuts import render, redirect
from .models import Medicine, PharmacistProfile

def create_medicine(request):
    routes = Medicine.ROUTES_OF_ADMINISTRATION  # Calling choices
    dosage_forms = Medicine.DOSAGE_FORMS  # Calling dosage choices

    if request.method == "POST":
        fk_pharmacy = PharmacistProfile.objects.get(fk_user=request.user)
        medicine_name = request.POST['medicine_name']
        brand_name = request.POST['brand_name']
        medicine_code = request.POST['medicine_code']
        drug_code = request.POST['drug_code']
        batch_lot_number = request.POST['batch_lot_number']
        strength_concentration = request.POST['strength_concentration']
        inactive_ingredients = request.POST['inactive_ingredients']
        dosage_form = request.POST['dosage_form']
        route_of_administration = request.POST['route_of_administration']
        recommended_dosage = request.POST['recommended_dosage']
        expiry_date = request.POST['expiry_date']
        manufacturing_date = request.POST['manufacturing_date']
        price_per_unit = request.POST['price_per_unit']
        stock_quantity = request.POST['stock_quantity']

        Medicine.objects.create(
            fk_pharmacy=fk_pharmacy,
            medicine_name=medicine_name,
            brand_name=brand_name,
            medicine_code=medicine_code,
            drug_code=drug_code,
            batch_lot_number=batch_lot_number,
            strength_concentration=strength_concentration,
            inactive_ingredients=inactive_ingredients,
            dosage_form=dosage_form,
            route_of_administration=route_of_administration,
            recommended_dosage=recommended_dosage,
            expiry_date=expiry_date,
            manufacturing_date=manufacturing_date,
            price_per_unit=price_per_unit,
            stock_quantity=stock_quantity,
            stock_status=True
        )

        return redirect('list_medicine')  # Redirect to a medicine list page

    return render(request, 'pharmacist/create_medicine.html', {'routes': routes, 'dosage_forms': dosage_forms})



from django.shortcuts import render
from .models import Medicine

def list_medicine(request):
    medicines = Medicine.objects.all()
    return render(request, 'pharmacist/list_medicine.html', {'medicines': medicines})

def toggle_stock_status(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    medicine.stock_status = not medicine.stock_status  # Toggle status
    medicine.save()
    return redirect('list_medicine')



############################################################################################

from collections import defaultdict
from django.core.paginator import Paginator
from django.core.paginator import Paginator
from django.shortcuts import render
from collections import defaultdict
from .models import Prescription

def prescription_list(request):
    prescriptions = Prescription.objects.select_related("fk_doctor", "fk_patient", "fk_medicine")

    # Filter by patient ID and date if provided
    patient_id = request.GET.get("patient_id", "").strip()
    created_date = request.GET.get("created_date", "").strip()

    if patient_id:
        prescriptions = prescriptions.filter(fk_patient__patient_id__icontains=patient_id)

    if created_date:
        prescriptions = prescriptions.filter(created_date__date=created_date)

    # Grouping prescriptions by Date and Time
    grouped_prescriptions = defaultdict(lambda: defaultdict(list))
    for pres in prescriptions:
        date_key = pres.created_date.strftime("%Y-%m-%d")  # Group by Date
        time_key = pres.created_date.strftime("%H:%M")  # Group by Time
        grouped_prescriptions[date_key][time_key].append(pres)

    # Convert to list for pagination
    grouped_items = [(date, dict(time_data)) for date, time_data in grouped_prescriptions.items()]
    paginator = Paginator(grouped_items, 5)  # 5 date groups per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "doctor/prescription_list.html", {
        "page_obj": page_obj,
        "patient_id": patient_id,
        "created_date": created_date
    })


from django.http import JsonResponse
from .models import PatientProfile

def search_patients(request):
    query = request.GET.get("q", "")
    patients = PatientProfile.objects.filter(patient_id__icontains=query)[:10]  # Limit to 10 results
    data = [{"id": patient.id, "patient_id": patient.patient_id} for patient in patients]
    return JsonResponse(data, safe=False)

def create_pres(request):
    days_choices = Prescription.DAYS_CHOICES  # Get choices
    doctor = DoctorProfile.objects.get(fk_user=request.user)  # Get logged-in doctor

    if request.method == "POST":
        patient_id = request.POST.get("patient")  # Get patient ID  
        disease_name = request.POST.get("disease_name")
        medicine_names = request.POST.getlist("medicine[]")  # Get all selected medicines
        days_to_take_list = request.POST.getlist("days_to_take[]")  # Get duration list
        
        # Debugging prints
        print(f"Received Patient ID: {patient_id}")
        print(f"Received Medicines: {medicine_names}")
        print(f"Received Days to Take: {days_to_take_list}")

        # Check if patient exists
        try:
            patient = PatientProfile.objects.get(patient_id=patient_id)
        except PatientProfile.DoesNotExist:
            print("Patient not found")
            return redirect("prescription_list")  # Redirect to prescription list instead of error

        # Loop through medicines and create prescriptions
        for idx, medicine_name in enumerate(medicine_names):
            medicine_name = medicine_name.strip()  # Trim spaces
            days_to_take = days_to_take_list[idx] if idx < len(days_to_take_list) else None

            medicine = Medicine.objects.filter(medicine_name__iexact=medicine_name).first()
            if not medicine:
                print(f"Medicine '{medicine_name}' not found (after trimming)")
                continue  # Skip missing medicines instead of returning an error

            # Create Prescription
            Prescription.objects.create(
                fk_doctor=doctor,
                fk_patient=patient,
                fk_medicine=medicine,
                disease_name=disease_name,
                days_to_take=days_to_take
            )

        print("✅ Prescription created successfully!")

        # Print all prescription data
        all_prescriptions = Prescription.objects.all()
        print("\n==== ALL PRESCRIPTIONS ====")
        for pres in all_prescriptions:
            print(f"Doctor: {pres.fk_doctor.fk_user.username}, "
                  f"Patient: {pres.fk_patient.patient_id}, "
                  f"Medicine: {pres.fk_medicine.medicine_name}, "
                  f"Days to Take: {pres.days_to_take}")
        print("===========================\n")

        return redirect("prescription_list")  # Redirect to the list page after success

    # Fetching data for dropdowns
    patients = PatientProfile.objects.all()
    medicines = Medicine.objects.all()

    return render(request, "doctor/create_pres.html", {
        "patients": patients,
        "medicines": medicines,
        "days_choices": days_choices
    })



############################################################ 15-03-2025


from django.shortcuts import render
from .models import Prescription, PatientProfile

def my_prescription(request):
    patient = PatientProfile.objects.get(fk_user=request.user)
    prescriptions = Prescription.objects.filter(fk_patient=patient).order_by('-created_date')
    return render(request, 'patients/my_prescriptions.html', {'prescriptions': prescriptions})

from django.http import JsonResponse
from .models import Prescription, PatientProfile


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Prescription, PatientProfile

def live_search_prescriptions(request):
    patient = get_object_or_404(PatientProfile, fk_user=request.user)
    prescriptions = Prescription.objects.filter(fk_patient=patient).order_by('-created_date')

    search_date = request.GET.get('date')
    search_disease = request.GET.get('disease_name')
    search_medicine = request.GET.get('medicine_name')

    if search_date:
        prescriptions = prescriptions.filter(created_date__date=search_date)
    if search_disease:
        prescriptions = prescriptions.filter(disease_name__icontains=search_disease)
    if search_medicine:
        prescriptions = prescriptions.filter(fk_medicine__medicine_name__icontains=search_medicine)

    data = {
        "prescriptions": [
            {
                "doctor": p.fk_doctor.fk_user.username,
                "medicine": p.fk_medicine.medicine_name,
                "disease": p.disease_name,
                "days": p.get_days_to_take_display(),
                "date": p.created_date.strftime("%Y-%m-%d"),
            }
            for p in prescriptions
        ]
    }
    return JsonResponse(data)



from django.shortcuts import render
from django.http import JsonResponse
from .models import PatientProfile, DoctorProfile

def token_list(request):
    query = request.GET.get('q', '').strip()
    tokens = Token_No.objects.all()

    if query:
        tokens = tokens.filter(
            Q(token_number__icontains=query) |
            Q(fk_doctor__fk_user__username__icontains=query) |
            Q(fk_patient__fk_user__username__icontains=query) |
            Q(created_date__icontains=query)
        )

    return render(request, 'phn/token_list.html', {'token': tokens})

from django.http import JsonResponse

from django.utils.timezone import now
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Token_No, PatientProfile, DoctorProfile

def generate_token(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient_id")
        doctor_id = request.POST.get("doctor_id")
        token_number = request.POST.get("token_number")

        if patient_id and doctor_id:
            patient = PatientProfile.objects.get(id=patient_id)
            doctor = DoctorProfile.objects.get(id=doctor_id)

            # Check if a token already exists for the same patient today
            existing_token = Token_No.objects.filter(
                fk_patient=patient,
                created_date__date=now().date()
            ).exists()

            if existing_token:
                return JsonResponse({'success': False, 'error': 'Token already generated for this patient today.'})

            # Create a new token if none exists for today
            token = Token_No.objects.create(token_number=token_number, fk_doctor=doctor, fk_patient=patient)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # If it's an AJAX request
                return JsonResponse({'success': True, 'token_number': token.token_number})
            else:
                return redirect('token_list')

    return render(request, 'phn/generate_token.html')




def search_patient(request):
    query = request.GET.get('query', '')
    patients = PatientProfile.objects.filter(patient_id__icontains=query)[:10]
    results = [{'id': p.id, 'patient_id': p.patient_id} for p in patients]
    return JsonResponse(results, safe=False)

def search_doctors(request):
    query = request.GET.get('query', '')
    doctors = DoctorProfile.objects.filter(fk_user__username__icontains=query)[:10]
    results = [{'id': d.id, 'name': d.fk_user.username} for d in doctors]
    return JsonResponse(results, safe=False)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Token_No

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Token_No, DoctorProfile

@login_required
def doctor_token_list(request):
    try:
        doctor = DoctorProfile.objects.get(fk_user=request.user)
        tokens = Token_No.objects.filter(fk_doctor=doctor)
    except DoctorProfile.DoesNotExist:
        tokens = []  # If the logged-in user doesn't have a DoctorProfile, show an empty list

    return render(request, 'doctor/token.html', {'tokens': tokens})
