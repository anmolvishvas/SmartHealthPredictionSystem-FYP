from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import DoctorForm
import datetime
from django.utils import timezone


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

        if user is not None:
            if type == "Patient":
                auth.login(request, user)
                return render(request, 'Patient_Dashboard.html')
            else:
                return render(request, 'loginPage.html')

    else:
        return render(request, 'registrationPage.html')


def LoginPage(request):
    error = ""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        sign = ""
        if user:
            try:
                sign = Patient.objects.get(user=user)
            except:
                pass
            if sign:
                login(request, user)
                error = "patient"
            else:
                pure = False
                try:
                    pure = Doctor.objects.get(status=1, user=user)
                except:
                    pass
                if pure:
                    login(request, user)
                    error = "doctor"
                else:
                    login(request, user)
                    error = "notmember"
            if user.is_staff:
                login(request, user)
                error = "admin"
        else:
            error = "not"
    d = {'error': error}
    return render(request, 'LoginPage.html', d)


def logout_user(request):
    logout(request)
    return redirect('welcome')

# admin views


@login_required(login_url="login")
def AdminDashboardPage(request):
    return render(request, 'Admin_Dashboard.html')


@login_required(login_url="login")
def AdminAddDoctorPage(request):
    error = ""
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
        category = request.POST["category"]

        if User.objects.filter(username=username).exists():
            error = "Username is already taken"
        if User.objects.filter(email=email).exists():
            error = "Email is already taken"
        user = User.objects.create_user(
            username=username, first_name=firstName, last_name=lastName, email=email, password=password)
        Doctor.objects.create(user=user, contact=contact,
                              dob=dob, address=address, image=photo, category=category, status=1)
        if user is not None:
            return redirect('admin_view_doctor')

        error = "error"
    d = {'error': error}
    return render(request, 'Admin_AddDoctors.html', d)


@login_required(login_url="login")
def AdminEditDoctorPage(request, pid):
    doc = Doctor.objects.get(id=pid)

    error = ""
    if request.method == 'POST':
        email = request.POST['email']
        contact = request.POST['contact']
        address = request.POST['address']
        category = request.POST['category']
        status = request.POST['userStatus']

        doc.user.email = email
        doc.contact = contact
        doc.category = category
        doc.address = address
        doc.status = status
        doc.user.save()
        doc.save()
        error = "create"
    dict = {'error': error, 'doc': doc}
    return render(request, 'Admin_EditDoctors.html', dict)


@login_required(login_url="login")
def delete_doctor(request, pid):
    doc = Doctor.objects.get(id=pid)
    BlacklistedDoctor.objects.create(user=doc.user, contact=doc.contact, dob=doc.dob,
                                     address=doc.address, image=doc.image, category=doc.category, status=2)
    doc.delete()
    return redirect('admin_view_doctor')


@login_required(login_url="login")
def AdminViewDoctorPage(request):
    doctors = Doctor.objects.all()
    doctor_dict = {'doctors': doctors}
    return render(request, 'Admin_ViewDoctors.html', doctor_dict)


@login_required(login_url="login")
def AdminViewPatientPage(request):
    patients = Patient.objects.all()
    patient_dict = {'patients': patients}
    return render(request, 'Admin_ViewPatient.html', patient_dict)


@login_required(login_url="login")
def delete_patient(request, pid):
    patient = Patient.objects.get(id=pid)
    BlacklistedPatient.objects.create(user=patient.user, contact=patient.contact, dob=patient.dob,
                                      address=patient.address, image=patient.image)
    patient.delete()
    return redirect('admin_view_patient')


@login_required(login_url="login")
def AdminViewPredictionResultsPage(request):
    return render(request, 'Admin_ViewPredictionResult.html')

# patient views


@login_required(login_url="login")
def PatientDashboardPage(request):
    user = request.user
    if user.is_authenticated:
        patient = user.patient
        context = {
            'username': user.username,
            'fullname': user.first_name + " " + user.last_name,
            'contact': patient.contact,
            'email': user.email,
            'address': patient.address,
            'image': patient.image
        }
        return render(request, 'Patient_Dashboard.html', context)
    else:
        return render(request, 'loginPage.html')


@login_required(login_url="login")
def PatientProfilePage(request):
    user = request.user
    if user.is_authenticated:
        patient = user.patient
        context = {
            'username': user.username,
            'fullname': user.first_name + " " + user.last_name,
            'contact': patient.contact,
            'email': user.email,
            'address': patient.address,
            'image': patient.image,
            'dob':patient.dob
        }
        return render(request, 'Patient_Profile.html', context)
    else:
        return render(request, 'loginPage.html')


@login_required(login_url="login")
def PatientEditProfilePage(request):
    message = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "patient"
    except:
        sign = Doctor.objects.get(user=user)
    if request.method == 'POST':
        firstname = request.POST['firstName']
        lastname = request.POST['lastName']
        email = request.POST['email']
        contact = request.POST['contact']
        address = request.POST['address']
        dob = request.POST['dob']
        try:
            image = request.FILES['image']
            sign.image = image
            sign.save()
        except:
            pass
        sign.user.first_name = firstname
        sign.user.last_name = lastname
        sign.user.email = email
        sign.contact = contact
        if error != "patient":
            category = request.POST['type']
            sign.category = category
            sign.save()
        sign.address = address
        sign.dob = datetime.datetime.strptime(dob, "%B %d, %Y").date()
        sign.user.save()
        sign.save()
        message = "create"
        return redirect('patient_profile')
    d = {'error':error,'message':message,'userr':sign}
    return render(request,'Patient_UpdateProfile.html',d)


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
