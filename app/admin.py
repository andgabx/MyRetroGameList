from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Game

admin.site.register(User, Profile, UserAdmin, Game)