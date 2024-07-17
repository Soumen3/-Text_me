from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomLoginForm, ForgotUsernameForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from verify_email.email_handler import send_verification_email
from django.core.mail import send_mail
from .models import Friend
from django.db.models import Q
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

User = get_user_model()

def forgot_username(request):
    if request.method == 'POST':
        form = ForgotUsernameForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                send_mail(
                    'Your Username',
                    f'Hello {user.first_name},\n\nYour username is: {user.username}',
                    'noreply<no_reply@domain.com>',
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Your username has been sent to your email.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'No user is associated with this email.')
    else:
        form = ForgotUsernameForm()
    return render(request, 'forgot_username/forgot_username.html', {'form': form})
        

def logout_user(request):
    logout(request)
    return redirect('login')

def verification_msg(request):
    message = "Email verification link sent to your email address. Please verify your email to login."
    return render(request, 'email_verification/verification_msg.html', {'msg': message})

def home(request):
    return render(request, 'chat/home.html')

@login_required(login_url='login')
def chat(request):
    return render(request, 'chat/chat.html')

@login_required(login_url='login')
def contacts(request):
    context = {}
    if request.method == "GET":
        if "friends" in request.GET:
            users= User.objects.filter(username__icontains=request.GET['friends'])
            user_first_names=User.objects.filter(first_name__icontains=request.GET['friends'])
            user_last_names=User.objects.filter(last_name__icontains=request.GET['friends'])
            all_users=users.union(user_first_names, user_last_names)
            friend_statuses = {}
            for user in all_users:
                friend_status = Friend.objects.filter(
                    (Q(user_1=request.user) & Q(user_2=user)) | 
                    (Q(user_1=user) & Q(user_2=request.user))
                ).first()
                friend_statuses[user.id] = friend_status.status if friend_status else 'unknown'
            
            print(friend_statuses)
            context['all_users'] = all_users
            context['friend_statuses'] = friend_statuses
            context['lst']=[1,2,3,4,5]


    return render(request, 'chat/contacts.html', context)

@login_required(login_url='login')
def profile(request):
    return render(request, 'chat/profile.html')