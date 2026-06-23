# REST is imported to make permissions managing easier
from rest_framework import permissions

# Checks if the user has rights to execute the request
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user