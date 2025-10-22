from rest_framework import permissions
from .models import ChatUser

class IsChatAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        sala_id = (
            view.kwargs.get('pk')
            or view.kwargs.get('sala_id')
            or request.data.get('sala')  # 👈 aceita também do body
        )
        if not sala_id:
            return False

        return ChatUser.objects.filter(
            sala_id=sala_id,
            user=request.user,
            is_admin=True
        ).exists()