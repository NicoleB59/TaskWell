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
    task = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20)
    addTask = models.DateTimeField(auto_now_add=True)
    editTask = models.DateTimeField(auto_now=True)
    deleteTask = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task

class Analytics(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date =  models.DateField()
    # Activity Data
    active_minutes = models.PositiveIntegerField(default=0)
    # Mood on a scale from 1 to 5
    mood_rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=3)
    # Goals
    goals_completed = models.PositiveIntegerField(default=0)
    total_goals = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Tracking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    water_intake = models.DecimalField(max_digits=4, decimal_places=1, help_text="Water intake in liters")
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=1, help_text="Sleep hours")
    weight = models.DecimalField(max_digits=5, decimal_places=1, help_text="Weight in kilograms")
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
