from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, "home.html")

@login_required
def resources(request):
    return render(request, 'resources.html') # Create this template

@login_required
def reports(request):
    return render(request, 'reports.html') # Create this template

@login_required
def notifications(request):
    return render(request, 'notifications.html')  # Create this template

@login_required
def profile(request):
    return render(request, 'profile.html')  # Create this template