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