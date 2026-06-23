from rest_framework import serializers
from .models import Event, Reservation

# This class serializes (help translating) Python object to JSON object

class EventSerializer(serializers.ModelSerializer):
    # Add the field 'available' but makes it read-only
    available = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date', 'total_seats', 'available']


class ReservationSerializer(serializers.ModelSerializer):
    event_details = EventSerializer(source='Event', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'event', 'event_details', 'status', 'created_at']
        read_only_fields = ['status']

    def validate(self, data):
        event = data['event']
        if event.available_seats <= 0:
            raise serializers.ValidationError('Sold out')
        return data
