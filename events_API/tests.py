import datetime
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Event, Reservation

User = get_user_model()

class EventAPITestCase(APITestCase):

    def setUp(self):
        # Create two test users
        self.user_admin = User.objects.create_superuser(username="admin", password="password123")
        self.user_mario = User.objects.create_user(username="mario", password="password123")

        # Create a test event
        self.event = Event.objects.create(
            name="Festival of the Sun",
            description="Festival curated by Rick Rubin",
            date=datetime.date(2026, 6, 21),
            total_seats=250
        )

    # ==========================================
    # PUBLIC AREA TESTS (EVENTS)
    # ==========================================

    def test_anonymous_user_can_view_event_list(self):
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify that the event created in setUp is in the list
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Festival of the Sun")

    # ==========================================
    # PRIVATE AREA TESTS (RESERVATIONS)
    # ==========================================

    def test_anonymous_user_CANNOT_book(self):
        booking_data = {"event": self.event.id}
        response = self.client.post('/api/reservations/', booking_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_user_can_book(self):
        # Log in the user 'mario' before making the request
        self.client.force_authenticate(user=self.user_mario)

        booking_data = {"event": self.event.id}
        response = self.client.post('/api/reservations/', booking_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify that the reservation actually exists in the dummy database
        self.assertEqual(Reservation.objects.filter(user=self.user_mario).count(), 1)

    def test_double_booking_prevention(self):
        self.client.force_authenticate(user=self.user_mario)
        booking_data = {"event": self.event.id}

        # First booking: must succeed (201 Created)
        response1 = self.client.post('/api/reservations/', booking_data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Second booking: must fail returning a 400 Bad Request error
        response2 = self.client.post('/api/reservations/', booking_data)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    # ==========================================
    # PRIVACY AND SECURITY TESTS (CANCELLATION)
    # ==========================================

    def test_reservation_privacy(self):
        # Create a reservation for the admin
        Reservation.objects.create(user=self.user_admin, event=self.event)

        # Log in Mario and go to the reservations list
        self.client.force_authenticate(user=self.user_mario)
        response = self.client.get('/api/reservations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Mario's list must be empty because he has not reserved any seays
        self.assertEqual(len(response.data), 0)

    def test_user_can_cancel_own_reservation(self):
        reservation = Reservation.objects.create(user=self.user_mario, event=self.event)

        self.client.force_authenticate(user=self.user_mario)
        response = self.client.post(f'/api/reservations/{reservation.id}/cancel/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh the object from the database to see if the status changed
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, 'CANCELLED')

    def test_user_CANNOT_cancel_others_reservation(self):
        admin_reservation = Reservation.objects.create(user=self.user_admin, event=self.event)

        # Log in Mario and try to mess up by canceling admin's ticket
        self.client.force_authenticate(user=self.user_mario)
        response = self.client.post(f'/api/reservations/{admin_reservation.id}/cancel/')

        # Must be blocked!
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Check that admin's ticket remained intact (CONFIRMED)
        admin_reservation.refresh_from_db()
        self.assertEqual(admin_reservation.status, 'CONFIRMED')