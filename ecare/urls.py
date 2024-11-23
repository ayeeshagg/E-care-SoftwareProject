"""
URL configuration for ecare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from hospital.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', home, name='home'),
    path('signup/', SignUp, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('shopmedicine/', shopmedicine, name='shopmedicine'),
    path('medicine_details/<int:medicine_id>/', medicine_details, name='medicine_details'),
    path('appointments/', appointments, name='appointments'),
    path('doctor/<int:doctor_id>/', doctor_details, name='doctor_details'),
    path('book_appointment/<int:schedule_id>/', book_appointment, name='book_appointment'),
    path('appointment_confirmation/<int:appointment_id>/', appointment_confirmation, name='appointment_confirmation'),
    path('hospital_details/<int:hospital_id>/', hospital_details, name='hospital_details'),

]
