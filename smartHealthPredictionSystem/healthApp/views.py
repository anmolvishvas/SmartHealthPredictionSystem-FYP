from django.shortcuts import render

# Create your views here.
# main views
def WelcomePage(request):
    return render(request, 'WelcomePage.html')

def RegistrationPage(request):
    return render(request, 'RegistrationPage.html')

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
