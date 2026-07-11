# REST is imported to make permissions managing easier
from rest_framework import permissions

# Checks if the user has rights to execute the request
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

# Checks if the user is an organizer
class IsOrganizer(permissions.BasePermission):
    def has_permission(self, request, view):
        # Ritorna True SOLO se è loggato ed è organizzatore/admin
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_organizer or request.user.is_staff)
        )