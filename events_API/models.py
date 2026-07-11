from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Custom User
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# Event
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    total_seats = models.PositiveIntegerField()

    @property
    def available_seats(self):
        booked = self.reservations.filter(status='CONFIRMED').count()
        return self.total_seats - booked

    def __str__(self):
        return f"{self.name} ({self.date.strftime('%Y-%m-%d')})"

# Reservation
class Reservation(models.Model):
    STATUS_CHOICES = [('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled')]

    # ATTENZIONE QUI: Usiamo settings.AUTH_USER_MODEL come ci ha chiesto il terminale
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reservations')
    status = models.CharField(choices=STATUS_CHOICES, default='CONFIRMED', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f'{self.user.username} - {self.event.name} - {self.status}'

# Automatically assigns a token when a user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)