from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
import datetime

# Create your views here.
# main views


def WelcomePage(request):
    return render(request, 'WelcomePage.html')


def RegistrationPage(request):
    if request.method == "POST":
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        dob = request.POST["dateOfBirth"]
        address = request.POST["address"]
        photo = request.FILES["image"]
        type = request.POST["userType"]
        date = datetime.date.today()

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken")
        user = User.objects.create_user(
            username=username, first_name=firstName, last_name=lastName, email=email, password=password)
        print(type)
        if type == "Patient":
            Patient.objects.create(
                user=user, contact=contact, dob=dob, address=address, image=photo)
        else:
            Doctor.objects.create(user=user, contact=contact,
                                  dob=dob, address=address, image=photo, status=2)

        # user.save()
        if user is not None:
            auth.login(request, user)
            return render(request, 'Admin_Dashboard.html')
    else:
        return render(request, 'registrationPage.html')


def LoginPage(request):
    return render(request, 'LoginPage.html')

# admin views


def AdminDashboardPage(request):
    return render(request, 'Admin_Dashboard.html')


def AdminAddDoctorPage(request):
    return render(request, 'Admin_AddDoctors.html')


def AdminEditDoctorPage(request):
    return render(request, 'Admin_EditDoctors.html')


def AdminViewDoctorPage(request):
    return render(request, 'Admin_ViewDoctors.html')


def AdminViewPatientPage(request):
    return render(request, 'Admin_ViewPatient.html')


def AdminViewPredictionResultsPage(request):
    return render(request, 'Admin_ViewPredictionResult.html')

# patient views


def PatientDashboardPage(request):
    return render(request, 'Patient_Dashboard.html')


def PatientProfilePage(request):
    return render(request, 'Patient_Profile.html')


def PatientEditProfilePage(request):
    return render(request, 'Patient_UpdateProfile.html')


def PatientFeedbackPage(request):
    return render(request, 'Patient_Feedback.html')


def PatientPredictionHistoryPage(request):
    return render(request, 'Patient_PredictionHistory.html')


def PatientHealthPredictionPage(request):
    return render(request, 'Patient_HealthPrediction.html')


def PatientHealthPredictionResultsPage(request):
    return render(request, 'Patient_HealthPredictionResult.html')


def PatientSettingsPage(request):
    return render(request, 'Patient_Settings.html')


# doctor views
def DoctorDashboardPage(request):
    return render(request, 'Doctor_Dashboard.html')


def DoctorProfilePage(request):
    return render(request, 'Doctor_Profile.html')


def DoctorEditProfilePage(request):
    return render(request, 'Doctor_EditProfile.html')


def DoctorViewPredictionResultsPage(request):
    return render(request, 'Doctor_PredictionResult.html')


def DoctorSettingsPage(request):
    return render(request, 'Doctor_Settings.html')
