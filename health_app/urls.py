from django.urls import path
from .views import *

urlpatterns = [   
   
   path('',landing_page,name="landing_page"),
   path('submit-message/', user_message_view, name='submit_message'),
   path('user_message_list',user_message_list,name="user_message_list"),
   path('user_message_delete/<int:id>/',user_message_delete,name="user_message_delete"),
   path('all_login',all_login,name="all_login"),
   path('all_register_page',all_register_page,name="all_register_page"),
   path('register/doctor/', register_doctor, name='register_doctor'),
   path('register/register_pharmacist/', register_pharmacist, name='register_pharmacist'),
   path('register/register_public_health_nurse/', register_public_health_nurse, name='register_public_health_nurse'),
   path('register/register_asha_worker/', register_asha_worker, name='register_asha_worker'),
   path('register/register_patient/', register_patient, name='register_patient'),
   path('register/register_junior_health_inspector/',register_junior_health_inspector, name='register_junior_health_inspector'),
   path('register/register_health_care/',register_healthcare, name='register_healthcare'),



   # DashBoard
   path('admin_dashboard', admin_dashboard, name='admin_dashboard'),
   path('ashaworker_dashboard', ashaworker_dashboard, name='asha_worker_dashboard'),
   path('doctor_dashboard', doctor_dashboard, name='doctor_dashboard'),
   path('junior_health_dashboard', junior_health_dashboard, name='junior_health_inspector_dashboard'),
   path('patient_dashboard', patient_dashboard, name='patient_dashboard'),
   path('pharmacist_dashboard', pharmacist_dashboard, name='pharmacist_dashboard'),
   path('public_nurse_dashboard', public_nurse_dashboard, name='public_health_nurse_dashboard'),
   path('health_dashboard', health_dashboard, name='health_dashboard'),

   path('logout/',logout_view, name='logout'),

   # List Of All Users
   
   path('list/healthcare/',list_healthcare, name='list_healthcare'),
   path('list/asha/',list_asha, name='list_asha'),
   path('list/doctors/', list_doctors, name='list_doctors'),
   path('list/public_health_nurses/',list_public_health_nurses, name='list_public_health_nurses'),
   path('list/patients/',list_patients, name='list_patients'),
   path('list/pharmacists/',list_pharmacists, name='list_pharmacists'),
   path('list/junior_health_inspectors/',list_junior_health_inspectors, name='list_junior_health_inspectors'),
   
   # Patient
   
   path('patient_report/',patient_report_create, name='patient_report'),
   path('patient_report_list/',patient_report_list, name='patient_report_list'),
   path('remove_report/<int:report_id>/', remove_report, name='remove_report'),
   path('search_doctor_patients/',search_doctor_patients, name='search_doctor_patients'),
   path('forgot_password/',forgot_password, name='forgot_password'),
   path('reset_password/<uidb64>/<token>/',reset_password, name='reset_password'),
   path('patient/enquiry/',user_contact, name='user_contact'),
   path('report/update/<int:report_id>/', report_update, name='report_update'),

   path('patient/find_my_doctor/',find_my_doctor, name='find_my_doctor'),
   
   
   # status
   path('health_status/<int:id>/',health_status, name='health_status'),
   path('ash_status/<int:id>/',ash_status, name='ash_status'),
   path('patient_status/<int:id>/',patient_status, name='patient_status'), 
   path('jhn_status/<int:id>/',jhn_status, name='jhn_status'),
   path('phn_status/<int:id>/',phn_status, name='phn_status'),
   path('doctor_status/<int:id>/',doctor_status, name='doctor_status'),
   path('pharmacist_status/<int:id>/',pharmacist_status, name='pharmacist_status'),



   # Health Care Doct All Users List Under Health Care 

   path('health/list-asha/',health_list_asha, name='h_list_asha'),
   path('health/list-doctors/',health_list_doctors, name='h_list_doctors'),
   path('health/list-nurse/', health_list_public_health_nurses, name='h_list_nurse'),
   path('health/list-pharmacists/',health_list_pharmacists, name='h_list_pharmacists'),
   path('health/list-inspectors/',health_list_junior_health_inspectors, name='h_list_inspectors'),



   # profiles  doctor
   
   path('doctor/doctors_profile/',doctors_profile, name='doctors_profile'),
   path('update-doctor-profile/', update_doctor_profile, name='update_doctor_profile'),
   path('create_doctor_attendance/',mark_doctor_attendance, name='mark_doctor_attendance'), 
   path('recognize_face/', recognize_face, name='recognize_face'),
   path('list_doctor_attendance/', my_doctor_attendance, name='my_doctor_attendance'),
   path('doct_list_all_att/',doct_list_all_att, name='doct_list_all_att'),

   # profiles  PHN

   path('PHN/phn_profile/',phn_profile, name='phn_profile'),
   path('update-phn-profile/', update_phn_profile, name='update_phn_profile'),
   path('myphn_attendance/', my_phn_attendance, name='my_phn_attendance'),
   path('mark_phn_attendance/',mark_phn_attendance, name='mark_phn_attendance'),
   path('phn_list_all_att/',phn_list_all_att, name='phn_list_all_att'),

   # profiles  ASHA   

   path('Asha/asha_profile/',asha_profile, name='asha_profile'),
   path('update-asha-profile/', update_asha_profile, name='update_asha_profile'),
   path('my_asha_attendance/', my_asha_attendance, name='my_asha_attendance'),
   path('mark_asha_attendance/',mark_asha_attendance, name='mark_asha_attendance'),


   # Pharmacist Urls

   path('Pharmacist/pharmacist_profile/',pharmacist_profile, name='pharmacist_profile'),
   path('update_pharmacist_profile/',update_pharmacist_profile, name='update_pharmacist_profile'),
   path('my_pharmacist_attendance/', my_pharmacist_attendance, name='my_pharmacist_attendance'),
   path('mark_pharmacist_attendance/',mark_pharmacist_attendance, name='mark_pharmacist_attendance'),


   # JHI Urls

   path('Jhi/jhi_profile',jhi_profile, name='jhi_profile'),
   path('update_jhi_profile/',update_jhi_profile, name='update_jhi_profile'),

   

   path('my_jhi_attendance/', my_jhi_attendance, name='my_jhi_attendance'),
   path('mark_jhi_attendance/',mark_jhi_attendance, name='mark_jhi_attendance'),


   path('asha_worker_list',asha_worker_list,name="asha_worker_list"),
   path('asha_worker_enquiry',save_household_data,name="save_household"),


   path('add-survey/', add_survey, name='add_survey'),
   path('survey_list/', survey_list, name='survey_list'),

   ########################################################

   path('phn_pregenent_add/', phn_pregenent_add, name='phn_pregenent_add'),
   path('phn_pregenent_list/', phn_pregenent_list, name='phn_pregenent_list'),

   path('maternal_visit_add/', maternal_visit_add, name='maternal_visit_add'),
   path('maternal_visit_list/', maternal_visit_list, name='maternal_visit_list'),

   path('add_child_growth_record/', add_child_growth_record, name='add_child_growth_record'),
   path('child_growth_list/', child_growth_list, name='child_growth_list'),
   path('update_child_growth_record/<int:id>', update_child_growth_record, name='update_child_growth_record'),

   path('register_vaccination/', register_vaccination, name='register_vaccination'),
   path('register_vaccination_list/', register_vaccination_list, name='register_vaccination_list'),

   path('vaccination_create/', vaccination_create, name='vaccination_create'),
   path('vaccination_list/', vaccination_list, name='vaccination_list'),
   path('vaccination_delete/<int:id>', vaccination_delete, name='vaccination_delete'),


   #########################

   path('add_bedridden/',add_bedridden, name='add_bedridden'),
   path('list_bedridden/',list_bedridden, name='list_bedridden'),

   path('schedule_bedridden_visit_list/',schedule_bedridden_visit_list, name='schedule_bedridden_visit_list'),
   path('schedule_bedridden_visit/',schedule_bedridden_visit, name='schedule_bedridden_visit'),

#######################################

   path('create_medicine/',create_medicine, name='create_medicine'),
   path('list_medicine/',list_medicine, name='list_medicine'),
   path('toggle-stock/<int:medicine_id>/', toggle_stock_status, name='toggle_stock'),


   path('create_pres/',create_pres, name='create_pres'),
   path("prescriptions/", prescription_list, name="prescription_list"),
   path("my_prescription/", my_prescription, name="my_prescription"),

   path("live-search-prescriptions/", live_search_prescriptions, name="live_search_prescriptions"),



   path("search-patients/", search_patients, name="search_patients"),




   path("generate_token/", generate_token, name="generate_token"),
   path("token_list/", token_list, name="token_list"),
   path("search_patient/", search_patient, name="search_patient"),
   path("search_doctors/", search_doctors, name="search_doctors"),

   path("doctor_token_list/", doctor_token_list, name="doctor_token_list"),

   path('complaints/', user_complaints, name='user_complaints'),
   path('admin-complaints/', admin_complaints, name='admin_complaints'),

   path('view_bedridden/', view_bedridden, name='view_bedridden'),

   path('admin-report_form/', report_form, name='report_form'),
   path('admin-report_list/', report_list, name='report_list'),

   path('survey-details/', survey_details, name='survey_details'),
   path('issue_medicine/', issue_medicine, name='issue_medicine'),

   path("stock_update/", stock_update, name="stock_update"),
   path("update_stock/", update_stock, name="update_stock"),



   path('d_contact/', d_contact, name='d_contact'),
   path('phn_contact/', phn_contact, name='phn_contact'),
   path('pharm_contact/', pharm_contact, name='pharm_contact'),
   path('pat_contact/', pat_contact, name='pat_contact'),
   path('j_contact/', j_contact, name='j_contact'),
   path('a_contact/', a_contact, name='a_contact'),


   #################################################################

   path('asha_complaints/', asha_complaints, name='asha_complaints'),

   path('pharmacist_complaints/', pharmacist_complaints, name='pharmacist_complaints'),

   path('doctor_complaints/', doctor_complaints, name='doctor_complaints'),

   path('jhi_complaints/', jhi_complaints, name='jhi_complaints'),

   path('phn_complaints/', phn_complaints, name='phn_complaints'),

   path('patients_complaints/', patients_complaints, name='patients_complaints'),
   
   
]





