from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Feedback)
admin.site.register(BlacklistedPatient)
admin.site.register(BlacklistedDoctor)
admin.site.register(Admin_Health_CSV)
admin.site.register(PredictionData)