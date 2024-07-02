from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),

	#-----------------Chat-----------------#
	path('chat/', views.chat, name='chat'),
	path('contacts/', views.contacts, name='contacts'),
	path('profile/', views.profile, name='profile'),

	#-----------------Authentication-----------------#
	path('login/', views.sign_in, name='login'),
	path('signup/', views.sign_up, name='signup'),
	path('logout/', views.logout_user, name='logout'),
]