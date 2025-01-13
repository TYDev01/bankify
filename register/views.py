from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import FormData, SignInData
from django.db import IntegrityError
from .models import UserForm  # Import custom model if used for auth

from django.contrib.auth.hashers import check_password



def index(request):
    return render(request, 'register/index.html')

# Signup View

def signup(request):
    if request.method == 'POST':
        form = FormData(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('register:signin')
            except IntegrityError:
                messages.error(request, 'User with this email or phone number already exists.')
        else:
            # Debugging: Print or log form errors
            print(form.errors)  # Prints errors to the terminal
            messages.error(request, f"Form errors: {form.errors}")  # Displays errors in messages
    else:
        form = FormData()
    return render(request, 'register/signup.html', {'form': form})

# Signin View

def signin(request):
    if request.method == 'POST':
        form = SignInData(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            try:
                # Find the user by username
                user_form = UserForm.objects.get(username=username)
                if check_password(password, user_form.password):  # Compare hashed passwords
                    # Log in user by storing session
                    request.session['user_id'] = user_form.id
                    messages.success(request, "Login successful!")
                    return render(request, 'dashboard/index.html')
                else:
                    messages.error(request, "Invalid details.")
            except UserForm.DoesNotExist:
                messages.error(request, "Invalid details.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = SignInData()
    return render(request, 'register/login.html', {'form': form})


# Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('signin')  # Redirect to login page


def transfer(request):
    return render(request, transfer)