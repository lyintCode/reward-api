from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'coins')

    fieldsets = UserAdmin.fieldsets + (
        ('Награды', {'fields': ('coins',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Награды', {'fields': ('coins',)}),
    )

admin.site.register(User, CustomUserAdmin)