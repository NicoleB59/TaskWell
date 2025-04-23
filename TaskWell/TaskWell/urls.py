"""
URL configuration for TaskWell project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view, name='index'),         # Root URL shows index.html
    path('index/', views.my_view, name='index'),   # /index/ also shows index.html
    path('task/', views.my_view2, name='task'),    # /task/ shows task.html
    path('analytics/', views.my_view3, name='analytics'),
    path('trackingpage/', views.my_view4, name='trackingpage'),
    path('notif/', views.my_view5, name='notif'),
    path('register/', views.my_view6, name='register'),
    path('login/', views.my_view7, name='login'),
    path('feedback/', views.my_view8, name='feedback'),
    path('reflectiveJ/', views.my_view9, name='reflectiveJ'),
    path('coachfeedback/', views.my_view9, name='coachfeedback'),
]

