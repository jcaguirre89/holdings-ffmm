from users.models import User
from users.serializers import UserSerializer
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    """
    `list`, `create`, `retrieve`, `update` and `destroy` actions for
    the User model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

