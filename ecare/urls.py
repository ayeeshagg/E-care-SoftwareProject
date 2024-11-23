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
    path('user_profile/', user_profile, name='user_profile'),
    path('cart/', cart, name='cart'),  
    path('cart/add/<int:medicine_id>/', add_to_cart, name='add_to_cart'),  
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'), 
    path('cart/clear/', clear_cart, name='clear_cart'),
    path('cart/increase/<int:cart_item_id>/', increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:cart_item_id>/', decrease_quantity, name='decrease_quantity'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
