from django.shortcuts import render


def my_view(request):
    return render(request, 'myapp/index.html')  # Home page

def my_view2(request):
    return render(request, 'myapp/task.html')   # Task page

def my_view3(request):
    return render(request, 'myapp/analytics.html') # analytics page

def my_view4(request):
    return render(request, 'myapp/trackingpage.html')

def my_view5(request):
    return render(request, 'myapp/notif.html')

def my_view6(request):
    return render(request, 'myapp/register.html')

def my_view7(request):
    return render(request, 'myapp/login.html')

# Premium User
def my_view8(request):
    return render(request, 'myapp/feedback.html')

def my_view9(request):
    return render(request, 'myapp/reflectiveJ.html')
# Health Coach

def my_view10(request):
    return render(request, 'myapp/coachfeedback.html')

