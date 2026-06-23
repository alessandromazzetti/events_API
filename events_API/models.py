from django.db import models
from django.contrib.auth.models import User

# Event
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    total_seats = models.PositiveIntegerField()

    # Find the available seats, @ lets us call the function without ()
    @property
    def available_seats(self):
        booked = self.reservations.filter(status='CONFIRMED').count()
        return self.total_seats - booked

    def __str__(self):
        return f"{self.title} ({self.date.strftime('%Y-%m-%d')})"

# Reservation
class Reservation(models.Model):
    STATUS_CHOICES = [('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reservations')
    status = models.CharField(choices=STATUS_CHOICES, default='CONFIRMED', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    # This stops the user from registering to the same event twice
    class Meta:
        unique_together = ('user', 'event')

    # Shows reservations in a formatted string
    def __str__(self):
        return f'{self.user.username} - {self.event} - {self.status}'