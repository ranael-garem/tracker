from rest_framework import viewsets
from rest_framework import views
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

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


class LoginView(views.APIView):
    """
    View responsible for logging in Users
    """

    def post(self, request, format=None):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if User.objects.filter(email=email).exists():
            username = User.objects.get(email=email).username

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    serialized = UserSerializer(
                        user, context={'request': request})
                    print serialized.data
                    return Response(serialized.data)
                else:
                    return Response({
                        'message': 'This account has been disabled.'
                    }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'message': 'Email or Password is incorrect'
        }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
