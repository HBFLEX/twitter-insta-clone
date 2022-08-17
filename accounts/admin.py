from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user', 'status']
    list_filter = ['user', 'status']


admin.site.register(Profile, ProfileAdmin)
