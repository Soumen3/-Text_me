from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

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

	#-----------------Password Reset-----------------#
	path('password_reset/', auth_views.PasswordResetView.as_view(template_name='forgot_password/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='forgot_password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='forgot_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='forgot_password/password_reset_complete.html'), name='password_reset_complete'),

	#-------------------Password Change-------------------#
	path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change/password_change_done.html'), name='password_change_done'),
]