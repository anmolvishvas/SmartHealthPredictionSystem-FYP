from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
import datetime
from validate_email import validate_email

import numpy as np
from scipy.stats import mode
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# chatbot
from django.http import JsonResponse
from .chatbot import chatbot_response

# chatbot


def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = chatbot_response(message)
        return JsonResponse({'response': response})
    else:
        return render(request, 'chat.html')

# Create your views here.
# main views


def WelcomePage(request):
    return render(request, 'WelcomePage.html')


def RegistrationPage(request):
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
        type = request.POST["userType"]
        date = datetime.date.today()
        category = request.POST["category"]
        # dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d").strftime('%B %d, %Y').date()

        if User.objects.filter(username=username).exists():
            error = "username_error"
        elif User.objects.filter(email=email).exists():
            error = "email_error"
        else:
            user = User.objects.create_user(
                username=username, first_name=firstName, last_name=lastName, email=email, password=password)
            if type == "Patient":
                Patient.objects.create(
                    user=user, contact=contact, dob=dob, address=address, image=photo)
            else:
                Doctor.objects.create(user=user, contact=contact,
                                      dob=dob, address=address, category=category, image=photo, status=2)

            if user is not None:
                if type == "Patient":
                    auth.login(request, user)
                    error = "patient"
                else:
                    error = "doctor"
    else:
        error = "not"
    d = {'error': error}

    return render(request, 'registrationPage.html', d)


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
    doctor_count = Doctor.objects.count()
    patient_count = Patient.objects.count()
    prediction_count = PredictionData.objects.count()
    feedback_count = Feedback.objects.count()
    user_count = doctor_count+patient_count
    return render(request, 'Admin_Dashboard.html', {'doctor_count': doctor_count, 'user_count': user_count, 'prediction_count': prediction_count, 'feedback_count': feedback_count})


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
            error = "username_error"
        elif User.objects.filter(email=email).exists():
            error = "email_error"
        else:
            user = User.objects.create_user(
                username=username, first_name=firstName, last_name=lastName, email=email, password=password)
            Doctor.objects.create(user=user, contact=contact,
                                  dob=dob, address=address, image=photo, category=category, status=1)
            if user is not None:
                return redirect('admin_view_doctor')
        # error = "error"
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
    prediction_data = PredictionData.objects.all()
    prediction_data_dict = {'prediction_data': prediction_data}
    return render(request, 'Admin_ViewPredictionResult.html', prediction_data_dict)


@login_required(login_url="login")
def delete_prediction_admin(request, pid):
    pred = PredictionData.objects.get(id=pid)
    pred.delete()
    return redirect('admin_view_prediction')


@login_required(login_url="login")
def AdminViewFeedbackPage(request):
    feedback = Feedback.objects.all()
    feedback_dict = {'feedbacks': feedback}
    return render(request, 'Admin_ViewFeedback.html', feedback_dict)


@login_required(login_url="login")
def delete_feedback(request, pid):
    feedback = Feedback.objects.get(id=pid)
    feedback.delete()
    return redirect('admin_view_feedback')


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
            'dob': patient.dob
        }
        return render(request, 'Patient_Profile.html', context)
    else:
        return render(request, 'loginPage.html')


@login_required(login_url="login")
def PatientEditProfilePage(request):
    message = ""
    user = User.objects.get(id=request.user.id)
    sign = Patient.objects.get(user=user)
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
        sign.address = address
        try:
            sign.dob = datetime.datetime.strptime(dob, "%B %d, %Y").date()
        except ValueError:
            # handle the error here, e.g. by setting a default date or displaying an error message to the user
            sign.dob = datetime.date(1900, 1, 1)
            message = "Invalid date format"
            d = {'message': message, 'userr': sign}
            return render(request, 'Patient_UpdateProfile.html', d)
        sign.user.save()
        sign.save()
        message = "create"
        return redirect('patient_profile')
    d = {'message': message, 'userr': sign}
    return render(request, 'Patient_UpdateProfile.html', d)


@login_required(login_url="login")
def PatientFeedbackPage(request):
    error = ""
    user = User.objects.get(id=request.user.id)
    sign = Patient.objects.get(user=user)
    if request.method == "POST":
        username = sign.user.username
        message = request.POST['msg']
        username = User.objects.get(username=username)
        Feedback.objects.create(user=username, messages=message)
        error = "create"
    d = {'message': error, 'userr': sign}
    return render(request, 'Patient_Feedback.html', d)


@login_required(login_url="login")
def PatientPredictionHistoryPage(request):
    prediction_data = PredictionData.objects.all()
    prediction_data_dict = {'prediction_data': prediction_data}
    return render(request, 'Patient_PredictionHistory.html', prediction_data_dict)


@login_required(login_url="login")
def delete_prediction(request, pid):
    pred = PredictionData.objects.get(id=pid)
    pred.delete()
    return redirect('patient_prediction_history')


@login_required(login_url="login")
def PatientHealthPredictionPage(request):
    predictionDetails = None
    listDiseases = []

    if request.method == "POST":
        for i, j in request.POST.items():
            if "csrfmiddlewaretoken" != i:
                listDiseases.append(i)
        # training.csv
        DATA_PATH = Admin_Health_CSV.objects.get(id=1)
        data = pd.read_csv(DATA_PATH.csv_file).dropna(axis=1)

        # Checking whether the dataset is balanced or not
        disease_counts = data["prognosis"].value_counts()
        temp_df = pd.DataFrame({
            "Disease": disease_counts.index,
            "Counts": disease_counts.values
        })

        plt.figure(figsize=(18, 8))
        sns.barplot(x="Disease", y="Counts", data=temp_df)
        plt.xticks(rotation=90)

        # Encoding the target value into numerical
        # value using LabelEncoder
        encoder = LabelEncoder()
        data["prognosis"] = encoder.fit_transform(data["prognosis"])

        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=24)

        symptoms = X.columns.values
        symptom_index = {}
        for index, value in enumerate(symptoms):
            symptom = " ".join([i.capitalize() for i in value.split("_")])
            symptom_index[symptom] = index

        data_dict = {
            "symptom_index": symptom_index,
            "predictions_classes": encoder.classes_
        }

        final_svm_model = SVC()
        final_nb_model = GaussianNB()
        final_rf_model = RandomForestClassifier(random_state=18)
        final_svm_model.fit(X, y)
        final_nb_model.fit(X, y)
        final_rf_model.fit(X, y)

        # Testing.csv
        DATA_PATH2 = Admin_Health_CSV.objects.get(id=2)
        test_data = pd.read_csv(DATA_PATH2.csv_file).dropna(axis=1)

        test_X = test_data.iloc[:, :-1]
        test_Y = encoder.transform(test_data.iloc[:, -1])

        svm_preds = final_svm_model.predict(test_X)
        nb_preds = final_nb_model.predict(test_X)
        rf_preds = final_rf_model.predict(test_X)

        final_preds = [mode([i, j, k])[0][0] for i, j,
                       k in zip(svm_preds, nb_preds, rf_preds)]

        print(f"Accuracy on Test dataset by the combined model\
        : {accuracy_score(test_Y, final_preds)*100}")

        cf_matrix = confusion_matrix(test_Y, final_preds)
        plt.figure(figsize=(12, 8))

        sns.heatmap(cf_matrix, annot=True)

        def predictDisease(symptoms):
            # # creating input data for the models
            input_data = [0] * len(data_dict["symptom_index"])
            for symptom in symptoms:
                index = data_dict["symptom_index"][symptom]
                input_data[index] = 1

            # reshaping the input data and converting it into suitable format for model predictions
            input_data = np.array(input_data).reshape(1, -1)

            # generating individual outputs
            rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[
                0]]
            nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[
                0]]
            svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[
                0]]

            # making final prediction by taking mode of all predictions
            final_prediction = mode(
                [rf_prediction, nb_prediction, svm_prediction])[0][0]
            predictions = {
                "RandomForestClassifier Prediction": rf_prediction,
                "GaussianNB Prediction": nb_prediction,
                "SVC Prediction": svm_prediction,
                "Final Prediction": final_prediction
            }
            return predictions

        # Testing the function
        predictionDetails = predictDisease(listDiseases)
        patient = Patient.objects.get(user=request.user)
        PredictionData.objects.create(patient=patient, prediction_accuracy=round(accuracy_score(test_Y, final_preds)*100, 2),
                                      result=predictionDetails["Final Prediction"], values_list=listDiseases, predict_for="General Health Prediction")
        # print(listDiseases)
    alldisease = ['Itching', 'Skin Rash', 'Nodal Skin Eruptions', 'Continuous Sneezing', 'Shivering', 'Chills', 'Joint Pain',	'Stomach Pain', 'Acidity', 'Ulcers On Tongue', 'Muscle Wasting', 'Vomiting', 'Burning Micturition', 'Fatigue', 'Weight Gain', 'Anxiety', 'Cold Hands And Feets', 'Mood Swings', 'Weight Loss', 'Restlessness', 'Lethargy', 'Patches In Throat', 'Irregular Sugar Level', 'Cough', 'High Fever', 'Sunken Eyes', 'Breathlessness', 'Sweating', 'Dehydration',	'Indigestion', 'Headache', 'Yellowish Skin', 'Dark Urine', 'Nausea', 'Loss Of Appetite', 'Pain Behind The Eyes', 'Back Pain', 'Constipation', 'Abdominal Pain', 'Diarrhoea', 'Mild Fever', 'Yellow Urine', 'Yellowing Of Eyes', 'Acute Liver Failure', 'Fluid Overload', 'Swelling Of Stomach', 'Swelled Lymph Nodes', 'Malaise', 'Blurred And Distorted Vision', 'Phlegm', 'Throat Irritation', 'Redness Of Eyes', 'Sinus Pressure', 'Runny Nose', 'Congestion', 'Chest Pain', 'Weakness In Limbs', 'Fast Heart Rate',	'Pain During Bowel Movements', 'Pain In Anal Region', 'Bloody Stool', 'Irritation In Anus', 'Neck Pain', 'Dizziness', 'Cramps', 'Bruising', 'Obesity', 'Swollen Legs', 'Swollen Blood Vessels', 'Puffy Face And Eyes', 'Enlarged Thyroid',
                  'Brittle Nails', 'Swollen Extremeties', 'Excessive Hunger', 'Extra Marital Contacts', 'Drying And Tingling Lips', 'Slurred Speech', 'Knee Pain', 'Hip Joint Pain', 'Muscle Weakness', 'Stiff Neck', 'Swelling Joints', 'Movement Stiffness', 'Spinning Movements', 'Loss Of Balance', 'Unsteadiness', 'Weakness Of One Body Side', 'Loss Of Smell', 'Bladder Discomfort', 'Continuous Feel Of Urine', 'Passage Of Gases', 'Internal Itching', 'Toxic Look (Typhos)',	'Depression', 'Irritability', 'Muscle Pain', 'Altered Sensorium', 'Red Spots Over Body', 'Belly Pain', 'Abnormal Menstruation', 'Dischromic Patches', 'Watering From Eyes', 'Increased Appetite', 'Polyuria', 'Family History', 'Mucoid Sputum', 'Rusty Sputum', 'Lack Of Concentration',	'Visual Disturbances', 'Receiving Blood Transfusion', 'Receiving Unsterile Injections', 'Coma', 'Stomach Bleeding',	'Distention Of Abdomen', 'History Of Alcohol Consumption', 'Fluid Overload', 'Blood In Sputum', 'Prominent Veins On Calf', 'Palpitations', 'Painful Walking', 'Pus Filled Pimples', 'Blackheads', 'Scurring', 'Skin Peeling', 'Silver Like Dusting', 'Small Dents In Nails', 'Inflammatory Nails', 'Blister', 'Red Sore Around Nose', 'Yellow Crust Ooze', 'Prognosis']
    return render(request, 'Patient_HealthPrediction.html', {'alldisease': alldisease, 'predictionDetails': predictionDetails})


@login_required(login_url="login")
def PatientSettingsPage(request):
    sign = 0
    user = User.objects.get(username=request.user.username)
    error = ""

    if not request.user.is_staff:
        sign = Patient.objects.get(user=user)
    message = ""
    if request.method == "POST":
        old_pass = request.POST['old_password']
        new_password = request.POST['new_password']
        c_new_password = request.POST['c_new_password']
        if not request.user.check_password(old_pass):
            message = "Incorrect"
        else:
            if new_password == c_new_password:
                update = User.objects.get(
                    username__exact=request.user.username)
                update.set_password(new_password)
                update.save()
                message = "yes"
            else:
                message = "not"
    d = {'error': error, 'message': message, 'data': sign}
    return render(request, 'Patient_Settings.html', d)


@login_required(login_url="login")
def PatientViewDoctorPage(request):
    doctors = Doctor.objects.all()
    doctor_dict = {'doctors': doctors}
    return render(request, 'Patient_ViewDoctors.html', doctor_dict)
# doctor views


@login_required(login_url="login")
def DoctorDashboardPage(request):
    user = request.user
    if user.is_authenticated:
        doctor = user.doctor
        context = {
            'username': user.username,
            'fullname': user.first_name + " " + user.last_name,
            'contact': doctor.contact,
            'email': user.email,
            'address': doctor.address,
            'image': doctor.image
        }
        return render(request, 'Doctor_Dashboard.html', context)
    else:
        return render(request, 'loginPage.html')


@login_required(login_url="login")
def DoctorProfilePage(request):
    user = request.user
    if user.is_authenticated:
        doctor = user.doctor
        context = {
            'username': user.username,
            'fullname': user.first_name + " " + user.last_name,
            'contact': doctor.contact,
            'email': user.email,
            'address': doctor.address,
            'image': doctor.image,
            'dob': doctor.dob,
            'category': doctor.category
        }
        return render(request, 'Doctor_Profile.html', context)
    else:
        return render(request, 'loginPage.html')


@login_required(login_url="login")
def DoctorEditProfilePage(request):
    message = ""
    user = User.objects.get(id=request.user.id)
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
        category = request.POST['type']
        sign.category = category
        sign.address = address
        sign.dob = datetime.datetime.strptime(dob, "%b. %d, %Y").date()
        sign.user.save()
        sign.save()
        message = "create"
        return redirect('doctor_profile')
    d = {'message': message, 'userr': sign}
    return render(request, 'Doctor_EditProfile.html', d)


@login_required(login_url="login")
def DoctorViewPredictionResultsPage(request):
    prediction_data = PredictionData.objects.all()
    prediction_data_dict = {'prediction_data': prediction_data}
    return render(request, 'Doctor_PredictionResult.html', prediction_data_dict)


@login_required(login_url="login")
def delete_prediction_doc(request, pid):
    pred = PredictionData.objects.get(id=pid)
    pred.delete()
    return redirect('doctor_view_prediction_result')


@login_required(login_url="login")
def DoctorSettingsPage(request):
    sign = 0
    user = User.objects.get(username=request.user.username)
    error = ""

    if not request.user.is_staff:
        sign = Doctor.objects.get(user=user)
    message = ""
    if request.method == "POST":
        old_pass = request.POST['old_password']
        new_password = request.POST['new_password']
        c_new_password = request.POST['c_new_password']
        if not request.user.check_password(old_pass):
            message = "Incorrect"
        else:
            if new_password == c_new_password:
                update = User.objects.get(
                    username__exact=request.user.username)
                update.set_password(new_password)
                update.save()
                message = "yes"
            else:
                message = "not"
    d = {'error': error, 'message': message, 'data': sign}
    return render(request, 'Doctor_Settings.html', d)
