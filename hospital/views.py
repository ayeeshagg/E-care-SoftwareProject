from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote, quote
from .models import *

# Create your views here.
def home(request):
    return render(request, 'index.html')

def SignUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different username.')
            return render(request, 'signup.html')

       
        user = User.objects.create_user(username=username, email=email, password=password)

        
        request.session['signup_username'] = username
        request.session['signup_email'] = email
        request.session['signup_password'] = password

        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('login')  
        else:
            messages.error(request, 'An error occurred while signing up. Please try again.')
            return render(request, 'Signup.html')
        
    return render(request, 'Signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the login credentials belong to a regular user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('home')  # Redirect to the booking page
         
        else:
            # Authentication failed, display an error message
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html')

@login_required
def logout(request):
    django_logout(request)
    return redirect('home')



def shopmedicine(request):
    selected_category = request.GET.get('category', None)
    
    if selected_category:
        # Decode the category to handle special characters
        selected_category = unquote(selected_category)
        # print(f"Decoded selected category: {selected_category}")
        
        medicines = Medicine.objects.filter(category=selected_category)
    else:
        medicines = Medicine.objects.all()
    
    categories = Medicine.CATEGORY_CHOICES
    medicines_by_category = {}

    for category, _ in categories:
        medicines_in_category = Medicine.objects.filter(category=category)
        medicines_by_category[category] = medicines_in_category

    # Encode the category name for the URL
    encoded_categories = [(quote(category), name) for category, name in categories]

    context = {
        'medicines': medicines,
        'medicines_by_category': medicines_by_category,
        'categories': encoded_categories,  # Pass encoded categories
        'selected_category': selected_category,
    }

    return render(request, 'Medicine.html', context)

@login_required
def user_profile(request):
    user = request.user
    
    # Get or create the user profile
    profile, created = Profile.objects.get_or_create(user=user)
    
    # Get orders, appointments, and carts related to the profile
    orders = Order.objects.filter(user=user)
    # Updated this to use the correct field, probably `patient`
    appointments = Appointment.objects.filter(patient=user)
    carts = Cart.objects.filter(user=user)

    context = {
        'user': user,
        'profile': profile,
        'orders': orders,
        'appointments': appointments,
        'carts': carts,
    }

    return render(request, 'Userprofile.html', context)

def appointments(request):
    doctors = Doctor.objects.all()
    hospitals = Hospital.objects.all()
    context = {
        'doctors': doctors,
        'hospitals': hospitals,
    }
    return render(request, 'Appointments.html', context)

# Doctor details and schedule view
def doctor_details(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    schedules = Schedule.objects.filter(doctor=doctor).order_by('hospital')

    context = {
        'doctor': doctor,
        'schedules': schedules,
    }
    return render(request, 'doctor_details.html', context)

# Appointment confirmation view
@login_required(login_url='login')
def appointment_confirmation(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'appointment_confirmation.html', {'appointment': appointment})


def hospital_details(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    doctors = hospital.schedules.values('doctor').distinct()
    doctor_list = Doctor.objects.filter(id__in=[d['doctor'] for d in doctors])
    
    context = {
        'hospital': hospital,
        'doctors': doctor_list,  # Pass the doctors related to the hospital
    }
    return render(request, 'hospital_details.html', context)

@login_required(login_url='login')
def cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    total_price = sum([item.total_price() for item in cart_items])  # Calculate total price of all cart items

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


@login_required(login_url='login')
def add_to_cart(request, medicine_id):
    user = request.user
    medicine = get_object_or_404(Medicine, id=medicine_id)

    # Check if cart item already exists for the user and medicine
    cart_item, created = Cart.objects.get_or_create(user=user, medicine=medicine)
    
    if not created:  # If it already exists, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')
   
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

@login_required
def clear_cart(request):
    user = request.user
    Cart.objects.filter(user=user).delete()  # Delete all cart items for the user
    return redirect('cart')

@login_required
def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # Remove item if quantity reaches 0
    return redirect('cart')

# Booking logic
@login_required(login_url='login')
def book_appointment(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    doctor = schedule.doctor
    hospital = schedule.hospital

    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        contact = request.POST.get('contact')

        # Check if this doctor is already booked at the selected date and time
        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            return HttpResponse("This time is already booked for the selected doctor.")

        # Create the appointment
        appointment = Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            hospital=hospital,
            schedule=schedule,
            patient_contact=contact,
            date=date,
            time=time,
            status='pending'
        )

        return redirect('appointment_confirmation', appointment_id=appointment.id)

    context = {
        'doctor': doctor,
        'schedule': schedule
    }
    return render(request, 'book_appointment.html', context)