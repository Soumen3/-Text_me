from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from verify_email.email_handler import send_verification_email

# Create your views here.

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    context = {}
    if request.method =="POST":
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')

    else:
        form = CustomLoginForm()
    context['form'] = form
    return render(request, 'auth/login.html', context)

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')
	
    context = {}
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            return redirect('verification_msg')
    else:
        form = CustomUserCreationForm()
    context['form'] = form
    return render(request, 'auth/signup.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')

def verification_msg(request):
    message = "Email verification link sent to your email address. Please verify your email to login."
    return render(request, 'email_verification/verification_msg.html', {'msg': message})

def home(request):
    return render(request, 'chat/home.html')

def chat(request):
    return render(request, 'chat/chat.html')

def contacts(request):
    return render(request, 'chat/contacts.html')

def profile(request):
    return render(request, 'chat/profile.html')