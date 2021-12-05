from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
    )
    email = serializers.EmailField(
        required=True
    )


    class Meta:
        model = User
        fields = (
            'password',
            'email'
        )


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        required=True,
    )
    current_password = serializers.CharField(
        required=True
    )
