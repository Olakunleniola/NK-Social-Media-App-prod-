from django.contrib import admin
from .models import Followers

class FollowersAdmin(admin.ModelAdmin):
    pass

admin.site.register(Followers, FollowersAdmin)