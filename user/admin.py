from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import User
from .forms import UserChangeForm, UserCreationForm

# Register your models here.

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        auth_admin.UserAdmin.fieldsets
        + (("INFO", {"fields": ("role","phone_number",)}),) 
        + (("Account Verification", {"fields": ("is_verified",)}),)
    )
    list_display = ["id","username","first_name", "last_name", "email", "phone_number","role",]
    search_fields = ["id","username","first_name", "last_name", "email", "phone_number","role",]
    ordering = ["-id"]
