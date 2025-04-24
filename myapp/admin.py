from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin
from .models import User, RegularUser, Task, Analytics, Tracking, Feedback, CoachFeedback, ManDash, ReflectiveJ, \
    Notification

# Register all models
admin.site.register(User, UserAdmin)
admin.site.register(RegularUser)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('taskID', 'description', 'status', 'addTask', 'editTask', 'deleteTask')
    search_fields = ('taskID', 'description', 'status')
    list_filter = ('status',)
admin.site.register(Task)

admin.site.register(Analytics)
admin.site.register(Tracking)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'date', 'weight', 'sleep_hours', 'mood_display', 'shortened_thoughts')

    def mood_display(self, obj):
        return obj.mood
    mood_display.short_description = 'Mood'

    def shortened_thoughts(self, obj):
        # Assuming 'obj' is an instance of the Feedback model and 'thoughts' is a field on that model
        # For example, truncate the 'thoughts' field to 50 characters
        return obj.thoughts[:50] + '...' if len(obj.thoughts) > 50 else obj.thoughts
    shortened_thoughts.short_description = 'Shortened Thoughts'

admin.site.register(Feedback, FeedbackAdmin)

class CoachFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_text', 'response', 'date_submitted', 'date_responded')
    search_fields = ('user__username', 'feedback_text')  # Add search functionality on user or feedback text
    list_filter = ('date_submitted', 'date_responded')  # Allows filtering based on dates
    ordering = ('-date_submitted',)  # Display the most recent feedback first

admin.site.register(CoachFeedback, CoachFeedbackAdmin)

# Custom Admin Interface for ManDash
class ManDashAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_count')  # Show user and the count of users in the dashboard
    search_fields = ('user__username', 'user__email')  # Make the username and email searchable
    actions = ['remove_selected_users']  # Add custom actions for removing users

    # Custom action for removing selected users
    def remove_selected_users(self, request, queryset):
        for man_dash in queryset:
            user_id = man_dash.user.id
            result = man_dash.remove_user(user_id)
            if result != "User not found.":
                self.message_user(request, f"Successfully removed {man_dash.user.username}.")
            else:
                self.message_user(request, f"Could not remove user {man_dash.user.username}.", level="error")

    remove_selected_users.short_description = "Remove selected users"  # Action description

# Register ManDash model with custom admin interface
admin.site.register(ManDash, ManDashAdmin)

class ReflectiveJAdmin(admin.ModelAdmin):
    list_display = ('user', 'entry_date')  # Show user and entry date
    search_fields = ('user__username', 'journal_entry')  # Make searching by username and journal content easier

# Register the model with the custom admin interface
admin.site.register(ReflectiveJ, ReflectiveJAdmin)

admin.site.register(Notification)