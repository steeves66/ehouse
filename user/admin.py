from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  # column displayed
  list_display = ('full_name', 'username', 'email', 'phone_number', 'is_staff', 'is_active')

  # column where system search
  search_fields = ("email__startswith", )

  # fields for form
  fields = ('last_name', 'first_name', 'username', 'email', 'phone_number', 'password', 'is_admin', 'is_staff', 'is_active', 'is_superadmin')
