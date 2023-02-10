from django.db import models
from django.contrib.auth.models import User

# Create your models here.
DOCTOR_STATUS = ((1, 'Authorize'), (2, 'UnAuthorize'))


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class BlacklistedPatient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Doctor(models.Model):
    status = models.IntegerField(DOCTOR_STATUS, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    dob = models.DateField(null=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class BlacklistedDoctor(models.Model):
    status = models.IntegerField(DOCTOR_STATUS, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    dob = models.DateField(null=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    messages = models.TextField(null=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.user.username