from rest_framework import permissions, viewsets

from .models import Profile
from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').all().order_by('-id')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
