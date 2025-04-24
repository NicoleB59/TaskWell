from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin
from .models import User, RegularUser, Task, Analytics, Tracking

# Register all models
admin.site.register(User, UserAdmin)
admin.site.register(RegularUser)
admin.site.register(Task)
admin.site.register(Analytics)
admin.site.register(Tracking)