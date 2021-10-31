from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, )
    confirmation_code = serializers.CharField(required=True, )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)
