from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event, Reservation
from .permissions import IsOwner, IsOrganizer
from .serializers import EventSerializer, ReservationSerializer


class EventListAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('date')
    serializer_class = EventSerializer

    def get_permissions(self):
        # Safe methods = read only methods, so everyone is allowed
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]

        # If the request is not safe this checks that the user who has made it is an organizer
        return [IsOrganizer()]


class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        # Safe methods = read only methods, so everyone is allowed
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]

        # If the request is not safe this checks that the user who has made it is an organizer
        return [IsOrganizer()]

class ReservationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        user = self.request.user

        if Reservation.objects.filter(event=event, user=user).exists():
            raise ValidationError('Reservation already exists')

        serializer.save(user=self.request.user)

# New view for cancelling (not a standard CRUD method, need to keep info about cancelled reservations)
class ReservationCancelAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner] # user must be logged in

    def post(self, request, pk):
        # Checks for the reservation (by ID)
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        # If found then checks permissions
        self.check_object_permissions(request, reservation)

        if reservation.status == 'CANCELLED':
            return Response({"message": "Already Cancelled"}, status=status.HTTP_400_BAD_REQUEST)

        # This updates the reservation status to 'cancelled' without deleting the reservation
        reservation.status = 'CANCELLED'
        reservation.save()
        return Response({"message": "Cancelled"})



