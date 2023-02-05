"""smartHealthPredictionSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from healthApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.WelcomePage, name='welcome'),
    path('login', views.LoginPage, name='login'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('registration', views.RegistrationPage, name='registration'),
    path('admin_dashboard', views.AdminDashboardPage, name="admin_dashboard"),
    path('admin_add_doctor', views.AdminAddDoctorPage, name='admin_add_doctor'),
    path('admin_view_doctor', views.AdminViewDoctorPage, name='admin_view_doctor'),
    path('admin_edit_doctor/<int:pid>/', views.AdminEditDoctorPage, name='admin_edit_doctor'),
    path('delete_doctor<int:pid>', views.delete_doctor, name="delete_doctor"),
    path('admin_view_patient', views.AdminViewPatientPage,
         name='admin_view_patient'),
    path('admin_view_prediction', views.AdminViewPredictionResultsPage,
         name='admin_view_prediction'),
    path('doctor_dashboard', views.DoctorDashboardPage, name='doctor_dashboard'),
    path('doctor_profile', views.DoctorProfilePage, name='doctor_profile'),
    path('doctor_edit_profile', views.DoctorEditProfilePage,
         name='doctor_edit_profile'),
    path('doctor_view_prediction_result', views.DoctorViewPredictionResultsPage,
         name='doctor_view_prediction_result'),
    path('doctor_settings', views.DoctorSettingsPage, name='doctor_settings'),
    path('patient_dashboard', views.PatientDashboardPage, name='patient_dashboard'),
    path('patient_profile', views.PatientProfilePage, name='patient_profile'),
    path('patient_edit_profile', views.PatientEditProfilePage,
         name='patient_edit_profile'),
    path('patient_feedback', views.PatientFeedbackPage, name='patient_feedback'),
    path('patient_prediction_history', views.PatientPredictionHistoryPage,
         name='patient_prediction_history'),
    path('patient_health_prediction', views.PatientHealthPredictionPage,
         name='patient_health_prediction'),
    path('patient_health_prediction_result', views.PatientHealthPredictionResultsPage,
         name='patient_health_prediction_result'),
    path('patient_settings', views.PatientSettingsPage, name='patient_settings'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
