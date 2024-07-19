from django.contrib import admin
from django.contrib.auth.models import User
from .models import Friend, UserProfile, Avatar, Site

# Register your models here.

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
#     # list_editable = ('is_active',)
    
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_1', 'user_2', 'status')
    list_filter = ('status',)
    search_fields = ('user_1__username', 'user_2__username')
    list_editable = ('status',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'avatar', 'about', 'phone', 'country', 'birth_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_editable = ('avatar', 'about', 'phone', 'country', 'birth_date')
    list_filter = ('country', 'birth_date')

@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_path', 'description')
    search_fields = ('description', 'file_path')
    list_editable = ('file_path', 'description')


admin.site.register(Site)