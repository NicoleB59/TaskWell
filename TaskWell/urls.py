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

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.my_view, name='index'),
    path('index/', views.my_view, name='index'),   # /index/ also shows index.html
    path('task/', views.task_list, name='task'),    # /task/ shows task.html
    path('task/<int:task_id>/', views.task_list, name='edit_task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('analytics/', views.analytics_health, name='analytics'),
    path('trackingpage/', views.tracking_health, name='trackingpage'),
    path('notif/', views.my_notif, name='notif'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('feedback/', views.feedback_user, name='feedback'),
    path('success_page/', views.success_page, name='success_page'),
    path('reflectiveJ/', views.ref_journal, name='reflectiveJ'),
    path('coachfeedback/', views.coach_feedback, name='coachfeedback'),
    path('feedback_success', views.feedback_success, name='feedback_success'),
    path('ManagerDashboard/', views.man_dash, name='ManagerDashboard'),
    path('remove_user/<int:user_id>/', views.remove_user, name='remove_user'),
    # URL for displaying the user notifications
    path('notifications/', views.user_notifications, name='notif'),

    # URL for marking a notification as read
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark-as-read'),

    # URL for creating a custom notification
    path('notifications/create/', views.create_custom_notification, name='create-custom-notification'),

    # URL for task assignment (as a sample, you can modify this)
    path('task/assigned/<int:task_id>/', views.task_assigned, name='task-assigned'),
]
