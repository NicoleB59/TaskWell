# Generated by Django 3.1.12 on 2025-04-24 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20250424_1341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analytics',
            name='active_minutes',
        ),
        migrations.RemoveField(
            model_name='analytics',
            name='goals_completed',
        ),
        migrations.RemoveField(
            model_name='analytics',
            name='mood_rating',
        ),
        migrations.RemoveField(
            model_name='analytics',
            name='total_goals',
        ),
    ]
