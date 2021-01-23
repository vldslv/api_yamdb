from uuid import uuid4

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import filters, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdmin
from .serializers import (ConfirmationCodeSerializer, AuthSerializer,
                          UserSerializer)


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = request.data.get('email')
    username = request.data.get('username')
    user, was_create = User.objects.get_or_create(
        username=username,
        email=email,)
    confirmation_code = default_token_generator.make_token(user)
    is_send = send_mail(
        'Yamdb no-reply',
        f'Your confirmation code: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,(email,))
    if not is_send:
        return Response(
            data={'error': 'Code not send. Please try leater'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if not default_token_generator.check_token(user, confirmation_code):
        return Response({'confirmation_code': 'Wrong confirmation code'},
                        status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    return Response({'token': f'{token}'}, status=status.HTTP_200_OK)


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    permission_classes = [IsAdmin]

    @action(detail=False,
            methods=['GET', 'PATCH'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        if request.method == 'PATCH': 
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
