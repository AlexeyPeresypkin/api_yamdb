import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from users.models import User
from .serializers import TokenSerializer, UserSerializer, SignUpSerializer
from rest_framework import viewsets, status, exceptions, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.permissions import IsAdministrator


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdministrator,)
    # filter_backends = [DjangoFilterBackend, ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['username', ]

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(email=instance.email, role=instance.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailSignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            confirmation_code = uuid.uuid4()
            email = serializer.validated_data.get('email')
            User.objects.create(
                email=email,
                username=str(email),
                confirmation_code=confirmation_code,
                is_active=False
            )
            send_mail(
                'confirmation_code',
                f'Your confirmation_code is: {confirmation_code}',
                DEFAULT_FROM_EMAIL, [email]
            )
            return Response(
                {
                    'result': 'A confirmation_code send on your email, please check'},
                status=status.HTTP_200_OK,
            )
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeConfirmView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            confirmation_code = serializer.validated_data.get(
                'confirmation_code')
            email = serializer.validated_data.get('email')
            try:
                user = User.objects.get(
                    confirmation_code=confirmation_code,
                    email=email
                )
            except exceptions.ValidationError:
                return Response(
                    {'detail': 'invalid confirmation_code or email'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'detail': f'Your refresh token is {refresh}, access token is {refresh.access_token}'},
                status=status.HTTP_200_OK
            )
