from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()


from TaskWell.views import TaskForm, TrackingForm, FeedbackForm
from myapp.models import Task, Tracking, Feedback, Notification

class SimpleTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123', role='regular')
        self.client.login(username='testuser', password='pass123')

    def test_home_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_task_form_valid(self):
        form = TaskForm(data={'taskID': 'T1', 'description': 'Test task', 'status': 'Pending'})
        self.assertTrue(form.is_valid())

    def test_tracking_form_valid(self):
        form = TrackingForm(data={'water_intake': 2.5, 'sleep_hours': 7, 'weight': 65})
        self.assertTrue(form.is_valid())

    def test_feedback_form_valid(self):
        form = FeedbackForm(data={'date': '2024-01-01', 'weight': 65, 'sleep_hours': 7, 'mood': 'Happy', 'thoughts': 'Feeling good'})
        self.assertTrue(form.is_valid())

    def test_tracking_view_post(self):
        response = self.client.post(reverse('trackingpage'), {
            'water_intake': 3,
            'sleep_hours': 8,
            'weight': 70
        })
        self.assertEqual(response.status_code, 302)  # Redirect after post

    def test_task_list_view_get(self):
        response = self.client.get(reverse('task'))
        self.assertEqual(response.status_code, 200)

    def test_feedback_submission_view(self):
        response = self.client.post(reverse('feedback_user'), {
            'date': '2024-01-01',
            'weight': 70,
            'sleep_hours': 6,
            'mood': 'Okay',
            'thoughts': 'Tired but okay'
        })
        self.assertEqual(response.status_code, 302)