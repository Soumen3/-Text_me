from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.home, name='home'),

	#-----------------Chat-----------------#
	path('chat/', views.chat, name='chat'),
	path('contacts/', views.contacts, name='contacts'),
	path('profile/', views.profile, name='profile'),

	#-----------------Authentication-----------------#
	path('accounts/login/', views.sign_in, name='login'),
	path('accounts/signup/', views.sign_up, name='signup'),
	path('accounts/logout/', views.logout_user, name='logout'),

	#-----------------Email Verification-----------------#
	path('verification/', include('verify_email.urls')),
	path('verification/msg/', views.verification_msg, name='verification_msg'),
]