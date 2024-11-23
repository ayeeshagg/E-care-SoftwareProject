from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Medicine)
admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(Schedule)
admin.site.register(Appointment)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)
admin.site.register(Cart)
