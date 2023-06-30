from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Userinfo

admin.site.register(Userinfo, UserAdmin)

# Register your models here.
