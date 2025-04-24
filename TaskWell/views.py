from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone

from TaskWell import settings
from myapp import models
from django import forms
from myapp.models import User, RegularUser, Task, Tracking, Analytics, Feedback, CoachFeedback, ManDash, ReflectiveJ, \
    Notification


def my_view(request):
    return render(request, 'myapp/index.html')  # Home page

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['taskID', 'description', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'status': forms.Select(choices=[('Pending', 'Pending'), ('Completed', 'Completed')]),
        }
@login_required
def task_list(request, task_id=None):
    tasks = Task.objects.filter(user=request.user)
    task_instance = None
    if task_id:
        task_instance = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task_instance)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task')
    else:
        form = TaskForm(instance=task_instance)

    return render(request, 'myapp/task.html', {
        'tasks': tasks,
        'form': form,
        'editing': task_instance is not None,
        'task_id': task_id,
    })

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('task')

def analytics_health(request):
    # Fetch all tracking data for the user
    analytics_data = Tracking.objects.filter(user=request.user)

    if analytics_data:
        context = {
            'analytics_data': analytics_data  # Pass all data to the template
        }
    else:
        context = {'message': 'No analytics data available'}

    return render(request, 'myapp/analytics.html', context)


class TrackingForm(forms.ModelForm):
    class Meta:
        model = Tracking
        fields = ['water_intake', 'sleep_hours', 'weight']

def tracking_health(request):
    if request.method == "POST":
        form = TrackingForm(request.POST)
        if form.is_valid():
            tracking_entry = form.save(commit=False)
            tracking_entry.user = request.user  # Assign the current user
            tracking_entry.save()
            return redirect('trackingpage')  # Redirect to the tracking page after saving
    else:
        form = TrackingForm()

    return render(request, 'myapp/trackingpage.html', {'form': form})

def my_notif(user, message):
    # Create a new notification
    Notification.objects.create(user=user, message=message)


def task_assigned(request, task_id):
    task = Task.objects.get(id=task_id)  # Example task retrieval
    user = task.assigned_user  # Assume task has an assigned user

    # Create a notification
    my_notif(user, f"New task '{task.title}' assigned to you.")

    return redirect('task-detail', task_id=task_id)


def user_notifications(request):
    notifications = request.user.notifications.filter(is_read=False)  # Get unread notifications
    return render(request, 'myapp/notif.html', {'notifications': notifications})


def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)

    # Mark the notification as read
    notification.mark_as_read()

    return redirect('notif')

class NotificationForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your custom message here...'}))

def create_custom_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            # Get the custom message from the form
            message = form.cleaned_data['message']
            user = request.user  # Assuming the logged-in user should receive the notification

            # Create the custom notification
            my_notif(user, message)

            # Redirect or show success message
            return redirect('notif')  # Redirect to the page where notifications are displayed

    else:
        form = NotificationForm()

    return render(request, 'myapp/notif.html', {'form': form})


class Register(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

def register_user(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            # Override role with the value from the radio buttons (accountType)
            role = request.POST.get('accountType')
            if role in dict(User.USER_ROLES).keys():
                user.role = role
            else:
                user.role = 'regular'  # default role if none selected

            user.save()

            if user.role == 'regular':
                RegularUser.objects.create(user=user, phone='', address='')

            messages.success(request, "Account created successfully. Log In")
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = Register()

    return render(request, 'myapp/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')

        else:
            form = AuthenticationForm()
            return render(request, 'myapp/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'myapp/login.html', {'form': form})

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['date', 'weight', 'sleep_hours', 'mood', 'thoughts']

# Premium User
@login_required
def feedback_user(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Manually associate the logged-in user with the feedback instance
            feedback = form.save(commit=False)
            feedback.user = request.user  # Set the user as the currently logged-in user
            feedback.save()  # Save the feedback record to the database
            return redirect('success_page')  # Redirect to a success page after form submission
    else:
        form = FeedbackForm()

    return render(request, 'myapp/feedback.html', {'form': form})

def success_page(request):
    return render(request, 'myapp/success_page.html')

def success_page(request):
    return render(request, 'myapp/success_page.html')

class ReflectiveJForm(forms.ModelForm):
    class Meta:
        model = ReflectiveJ
        fields = ['journal_entry']  # Only allow users to input their journal entry

def ref_journal(request):
    if request.method == "POST":
        form = ReflectiveJForm(request.POST)
        if form.is_valid():
            reflective_journal = form.save(commit=False)
            reflective_journal.user = request.user  # Associate the current user
            reflective_journal.save()
            return redirect('success_page')  # Redirect after submission
    else:
        form = ReflectiveJForm()

    return render(request, 'myapp/reflectiveJ.html', {'form': form})

# Health Coach
@login_required
def coach_feedback(request):
    coachFeed_data = CoachFeedback.objects.filter(user=request.user).order_by('-date_submitted')

    if request.method == 'POST':
        # Check for coach response
        feedback_id = request.POST.get('feedback_id')
        response_text = request.POST.get('response_text')

        # Check for user response
        user_response_id = request.POST.get('user_response_id')
        user_response_text = request.POST.get('user_response_text')

        # Coach is responding
        if feedback_id and response_text:
            feedback = CoachFeedback.objects.get(id=feedback_id)
            feedback.response = response_text
            feedback.date_responded = timezone.now()
            feedback.save()
            return redirect('feedback_success')

        # User is responding to coach's message
        elif user_response_id and user_response_text:
            feedback = CoachFeedback.objects.get(id=user_response_id, user=request.user)
            feedback.user_response = user_response_text
            feedback.date_user_responded = timezone.now()
            feedback.save()
            return redirect('feedback_success')

        # User submitting new feedback
        else:
            feedback_text = request.POST.get('feedback_text')
            if feedback_text:
                CoachFeedback.objects.create(user=request.user, feedback_text=feedback_text)
                return redirect('feedback_success')

    context = {
        'coachFeed_data': coachFeed_data
    }
    return render(request, 'myapp/coachfeedback.html', context)


def feedback_success(request):
    return render(request, 'myapp/feedback_success.html')

# manager dash

def man_dash(request):
    # Fetch all users for the manager to oversee
    users = User.objects.all()

    # Optionally, fetch the admin dashboard data (if applicable)
    man_dashboard = ManDash.objects.filter(user=request.user).first()

    context = {
        'users': users,  # List of all users
        'admin_dashboard': man_dashboard,  # Admin dashboard data (if any)
    }

    return render(request, 'myapp/ManagerDashboard.html', context)


def remove_user(request, user_id):
    try:
        man_dash = ManDash.objects.get(user_id=user_id)  # Get the user associated with the 'ManDash' entry
        user = man_dash.user  # Get the user from ManDash model

        # If the user is trying to delete themselves, handle that case
        if user == request.user:
            messages.error(request, "You cannot delete yourself.")
        else:
            man_dash.remove_user(user_id)  # Call the method to remove the user from the model

            # Show success message to the admin
            messages.success(request, f"Successfully removed {user.username}.")

    except ManDash.DoesNotExist:
        messages.error(request, "User does not exist.")

    # Redirect back to the Manager Dashboard
    return redirect('ManagerDashboard')  # This will use the URL pattern name from your urls.py


