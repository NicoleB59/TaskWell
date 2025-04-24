from django.db import models

# Register your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.

class User(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('regular', 'regularUser'),
        ('premium', 'premiumUser'),
        ('coach', 'healthCoach'),
    )
    role = models.CharField(max_length=50, choices=USER_ROLES)

    groups = models.ManyToManyField(
        Group,
        related_name='regular_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='regular_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class RegularUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)
    address = models.TextField()

    def __str__(self):
        return self.user.get_full_name()

class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    taskID = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20)
    addTask = models.DateTimeField(auto_now_add=True)
    editTask = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task ID: {self.taskID}, Description: {self.description}, Status: {self.status}, Added: {self.addTask}, Edited: {self.editTask}"

class Analytics(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        # Attempt to get tracking data for this user and date
        try:
            tracking_data = Tracking.objects.get(user=self.user, date=self.date)
            # If tracking data exists, include it in the string
            return (f"User: {self.user.username} - Date: {self.date} - "
                    f"Water Intake: {tracking_data.water_intake or 'No data'}L, "
                    f"Sleep Hours: {tracking_data.sleep_hours or 'No data'}hrs, "
                    f"Weight: {tracking_data.weight or 'No data'}kg, ",
            )
        except Tracking.DoesNotExist:
            # If no tracking data exists, show just the analytics data
            return (f"User: {self.user.username} - Date: {self.date} - "
                    f"Active Minutes: {getattr(self, 'active_minutes', 'No data')}, "
                    f"Mood: {getattr(self, 'mood_rating', 'No data')}, "
                    f"Goals Completed: {getattr(self, 'goals_completed', 'No data')}/"
                    f"{getattr(self, 'total_goals', 'No data')}")

class Tracking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    water_intake = models.DecimalField(max_digits=4, decimal_places=1, help_text="Water intake in liters")
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=1, help_text="Sleep hours")
    weight = models.DecimalField(max_digits=5, decimal_places=1, help_text="Weight in kilograms")
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (f"User: {self.user.username}, Date: {self.date}, "
                f"Water Intake: {self.water_intake}L, Sleep Hours: {self.sleep_hours}hrs, "
                f"Weight: {self.weight}kg")


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    weight = models.DecimalField(max_digits=5, decimal_places=1, help_text="Weight in kilograms")
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=1, help_text="Sleep hours")
    thoughts = models.TextField()
    mood = models.CharField(
        max_length=10,
        choices=[
            ('very_bad', 'Very Bad'),
            ('bad', 'Bad'),
            ('neutral', 'Neutral'),
            ('good', 'Good'),
            ('very_good', 'Very Good'),
        ],
        help_text="Mood rating",
    )

    def __str__(self):
        return (f"Feedback from {self.user} on {self.date}: Weight={self.weight}kg, "
                f"Sleep={self.sleep_hours}hrs, "
                f"Mood={self.mood}, "
                f"Thoughts='{self.thoughts[:50]}'")


class CoachFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    response = models.TextField(blank=True, null=True)  # Coach's reply
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_responded = models.DateTimeField(auto_now=True)
    user_response = models.TextField(null=True, blank=True)
    date_user_responded = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.feedback_text} - {self.date_submitted} - {self.date_responded}"

class ManDash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Admin user
    user_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Manager Dashboard for {self.user.username}"

    # Method to update the user count in the admin dashboard
    def update_user_count(self):
        self.user_count = User.objects.all().count()
        self.save()

    # Method to add a user (Admin can add users to the system)
    def add_user(self, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        self.update_user_count()
        return user

    # Method to remove a user (Admin can remove a user)
    def remove_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            # Ensure that the user is not the one performing the deletion (if needed)
            if user == self.user:
                return "You cannot delete yourself."
            user.delete()  # Delete the user from the database
            self.update_user_count()  # Update the user count
        except User.DoesNotExist:
            return "User not found."

class ReflectiveJ(models.Model):
    # Link the reflective journal entry to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # The content the user submits for reflection
    journal_entry = models.TextField()

    # Date when the entry was created
    entry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reflective Journal Entry by {self.user.username} on {self.entry_date.strftime('%Y-%m-%d')}"


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"

    def mark_as_read(self):
        self.is_read = True
        self.save()


