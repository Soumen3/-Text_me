from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomLoginForm, ForgotUsernameForm, ProfileUpadateForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from verify_email.email_handler import send_verification_email
from django.core.mail import send_mail
from .models import Friend, UserProfile, Avatar
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
    context = {}
    friends = Friend.objects.filter(Q(user_1=request.user, status="accepted") | Q(user_2=request.user, status="accepted")).order_by('-id')
    context['friends'] = friends
    profiles = User.objects.filter(id__in=[friend.user_1.id if friend.user_1 != request.user else friend.user_2.id for friend in friends])
    context['friend_profiles'] = profiles
    print(profiles)
    print(friends)
    return render(request, 'chat/chat.html', context)

@login_required(login_url='login')
def chat_room(request, username, id):
    context = {}

    friends = Friend.objects.filter(Q(user_1=request.user, status="accepted") | Q(user_2=request.user, status="accepted")).order_by('-id')
    context['friends'] = friends
    profiles = User.objects.filter(id__in=[friend.user_1.id if friend.user_1 != request.user else friend.user_2.id for friend in friends])
    context['friend_profiles'] = profiles

    
    friend = User.objects.get(username=username, id=id)
    context['friend'] = friend
    return render(request, 'chat/chat_room.html', context)

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
                
            context['all_users'] = all_users
            context['friend_statuses'] = friend_statuses
        else:
            friends = Friend.objects.filter(Q(user_1=request.user, status="accepted") | Q(user_2=request.user, status="accepted")).order_by('-id')
            context['friends'] = friends
            profiles = UserProfile.objects.filter(user__in=[friend.user_1 if friend.user_1 != request.user else friend.user_2 for friend in friends])
            context['profiles'] = profiles
            
    return render(request, 'chat/contacts.html', context)

@login_required(login_url='login')
def friend_request(request):
    context={}
    friends = Friend.objects.filter(Q(user_2=request.user, status='pending')).order_by('-id')
    context['friends'] = friends

    return render(request, 'chat/friend_request.html', context)


@login_required(login_url='login')
def friend_request_send(request):
    context={}
    friends = Friend.objects.filter(Q(user_1=request.user, status='pending')).order_by('-id')
    context['friends'] = friends

    return render(request, 'chat/friend_request_send.html', context)



@login_required(login_url='login')
def profile(request):
    context = {}

    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user, avatar=Avatar.objects.get(id=10))
        profile.save()
    context['profile'] = profile

    all_fields_set = all(getattr(profile, field.name) for field in UserProfile._meta.get_fields())
    if not all_fields_set:
        context['all_fields_set'] = False
    else:
        context['all_fields_set'] = True

    return render(request, 'chat/profile.html', context)

@login_required(login_url='login')
def edit_profile(request, user_id):
    if request.user.id != user_id:
        return redirect('home')
    
    context = {}
    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        updateForm = ProfileUpadateForm(request.POST, request.FILES, instance=profile)
        if updateForm.is_valid():
            updateForm.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating profile')
    profile = UserProfile.objects.get(user=request.user)
    updateForm = ProfileUpadateForm(instance=profile)
    context['updateForm'] = updateForm
    return render(request, 'chat/edit_profile.html', context)


@login_required(login_url='login')
def change_avatar(request, user_id):
    context= {}
    if request.user.id != user_id:
        return redirect('home')
    
    if request.method == 'POST':
        print(request.POST)
        avatar_id = request.POST.get('selected_avatar')
        print(avatar_id)
        profile = UserProfile.objects.get(user=request.user)
        profile.avatar = Avatar.objects.get(id=avatar_id)
        profile.save()
        return redirect('profile')
    avatars = Avatar.objects.all()
    context['avatars'] = avatars
    return render(request, 'chat/change_avatar.html', context)

@login_required(login_url='login')
def contact_profile(request, username, id):
    context={}
    contact_user= User.objects.get(username=username, id=id)
    context['user']=contact_user
    profile = UserProfile.objects.get(user=contact_user)
    context['profile']=profile
    return render(request, 'chat/contact_profile.html', context)



@csrf_exempt
def send_request(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        friend = Friend(user_1=request.user, user_2=user, status='pending')
        friend.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@csrf_exempt
def accept_request(request, user_id):
    if request.method == "POST":
        friend = Friend.objects.filter(Q(user_1_id=user_id) & Q(user_2=request.user)).first()
        friend.status = 'accepted'
        friend.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@csrf_exempt
def reject_request(request, user_id):
    if request.method == "POST":
        friend = Friend.objects.filter(Q(user_1_id=user_id) & Q(user_2=request.user)).first()
        friend.status = 'rejected'
        friend.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@csrf_exempt
def cancel_request(request, user_id):
    print(user_id)
    if request.method == "POST":
        friend = Friend.objects.filter(Q(user_1=request.user) & Q(user_2_id=user_id)).first()
        friend.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})