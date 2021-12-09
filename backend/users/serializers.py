from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Follow

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        read_only=True
    )

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

    def get_is_subscribed(self, obj):
        request = self.context['request']
        user = self.context['request'].user
        if request and user.is_authenticated:
            return Follow.objects.filter(user=user).exists()
        return False


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
