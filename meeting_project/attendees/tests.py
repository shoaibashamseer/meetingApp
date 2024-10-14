from django.test import TestCase

# Create your tests here.
# attendees/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Attendee, Stall, StallVisit

class StallVisitTests(TestCase):

    def setUp(self):
        # Create a test user (stall keeper)
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test stall
        self.stall = Stall.objects.create(name='Test Stall', keeper=self.user)

        # Create a test attendee
        self.attendee = Attendee.objects.create(
            unique_id='123456',
            name='John Doe',
            place='City',
            job='Engineer',
            phone='1234567890',
            num_persons=1,
            prize='None'
        )

        # Create a test client
        self.client = Client()

    def test_stall_keeper_login(self):
        # Test stall keeper login
        response = self.client.post('/attendees/stall_keeper_login/', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to stall dashboard
        self.assertRedirects(response, '/attendees/stall_dashboard/')

    def test_scan_attendee(self):
        # Log in the stall keeper
        self.client.login(username='testuser', password='testpassword')

        # Scan the attendee's QR code
        response = self.client.get(f'/attendees/scan_attendee/{self.attendee.unique_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'attendees/scan_success.html')

        # Check that the StallVisit record was created
        visit = StallVisit.objects.filter(attendee=self.attendee, stall=self.stall).first()
        self.assertIsNotNone(visit)
        self.assertEqual(visit.attendee, self.attendee)
        self.assertEqual(visit.stall, self.stall)
