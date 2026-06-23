from django.urls import path
from . import views

# Shows the correct view based off the URL

urlpatterns = [
    path('events/', views.EventListAPIView.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventDetailAPIView.as_view(), name='event-detail'),
    path('reservations/', views.ReservationListCreateAPIView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/cancel/', views.ReservationCancelAPIView.as_view(), name='reservation-cancel'),
]