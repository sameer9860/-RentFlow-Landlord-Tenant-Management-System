from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def auth_status(request):
    profile = getattr(request.user, 'profile', None)

    return Response({
        'is_authenticated': True,
        'user_id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'role': profile.role if profile else None,
    })
