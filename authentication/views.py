from rest_framework import viewsets
from rest_framework.response import Response

from django.contrib.auth.models import User

from authentication.serializers import UserSerializer
from authentication.permissions import IsCurrentUser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = IsCurrentUser,

    def update(self, request, *args, **kwargs):
        """
        Overiden update method to return a success message
        if password is updated
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if request.data.get('password', None):
            data = serializer.data
            data.update({'message': 'Password Changed Successfully'})

        return Response(data)
