from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from myapp import models
from django import forms
from myapp.models import User, RegularUser, Task


def my_view(request):
    return render(request, 'myapp/index.html')  # Home page

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task','description','status']
@login_required
def task_list(request):
    
def my_view3(request):
    return render(request, 'myapp/analytics.html') # analytics page

def my_view4(request):
    return render(request, 'myapp/trackingpage.html')

def my_view5(request):
    return render(request, 'myapp/notif.html')

class Register(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

def my_view6(request):
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


def my_view7(request):
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


# Premium User
def my_view8(request):
    return render(request, 'myapp/feedback.html')

def my_view9(request):
    return render(request, 'myapp/reflectiveJ.html')
# Health Coach

def my_view10(request):
    return render(request, 'myapp/coachfeedback.html')

# manager dash
def my_view11(request):
    return render(request, 'myapp/ManagerDashboard.html')

