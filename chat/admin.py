from django.contrib import admin
from django.contrib.auth.models import User
from .models import Friend

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