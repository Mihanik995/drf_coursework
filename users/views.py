from rest_framework import generics

from users.serializers import UserRegisterSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
