from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

# @admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    # list_editable = ('is_active',)
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)