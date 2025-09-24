from rest_framework import permissions

class IsMessageOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to view their own messages.
    Assumes the view has a `get_object()` method that returns a message instance.
    """

    def has_object_permission(self, request, view, obj):
        # Only allow access if the user is either the sender or the receiver
        user = request.user
        return user.is_authenticated() and (obj.sender == user or obj.receiver == user)
    
class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow users to access conversations they are part of.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return user.is_authenticated() and obj.participants.filter(id=user.id).exists()
        return user.is_authenticated()