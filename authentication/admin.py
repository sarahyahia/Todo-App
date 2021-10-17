from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('email','username', 'is_staff',)
    search_fields = ('email','username', 'is_staff',)
    list_per_page = 2

admin.site.register(User, UserAdmin)