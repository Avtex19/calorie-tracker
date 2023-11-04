from django.contrib import admin

from .models import Lunch, Breakfast, Dinner, UserProfile

# Register your models here.
admin.site.register(Lunch)
admin.site.register(Breakfast)
admin.site.register(Dinner)
admin.site.register(UserProfile)
