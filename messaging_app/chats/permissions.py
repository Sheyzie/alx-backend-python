from rest_framework import permissions

class IsMessageOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to view their own messages.
    Assumes the view has a `get_object()` method that returns a message instance.
    """

    def has_object_permission(self, request, view, obj):
        # Only allow access if the user is either the sender or the receiver
        return obj.sender == request.user or obj.receiver == request.user
    
class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow users to access conversations they are part of.
    """

    def has_object_permission(self, request, view, obj):
        # Assuming 'participants' is a ManyToManyField or list of users in the conversation
        return request.user in obj.participants.all()