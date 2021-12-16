from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (UserSerializer, SignUpSerializer,
                          SetPasswordSerializer, SubscribeSerializer)
from .models import User
from recipes.models import Follow
from api.serializers import FollowSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    @action(methods=['get'], detail=False,
            url_path='me', url_name='me',
            permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False,
            url_path='set_password', url_name='set_password',
            permission_classes=[IsAuthenticated])
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(data=self.request.data)
        new_password = self.request.data.get('new_password')
        if serializer.is_valid():
            user = get_object_or_404(User, pk=self.request.user.id)
            user.password = new_password
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False,
            url_path='subscriptions', url_name='subscriptions',
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request, *args, **kwargs):
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscribeSerializer(
                queryset,
                context={'request': request},
                many=True
            )
            self.get_paginated_response(serializer.data)
        serializer = SubscribeSerializer(
            queryset,
            context={'request': request},
            many=True
        )    
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get', 'delete'], detail=False,
            url_path=r'(?P<id>\d+)/subscribe',
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        following = get_object_or_404(User, id=self.kwargs.get('id'))
        if request.method == 'GET':
            subscribe_serializer = FollowSerializer(
                data={'user': user.id, 'following': following.id}
            )
            subscribe_serializer.is_valid(raise_exception=True)
            subscribe_serializer.save()
            serializer = SubscribeSerializer(
                following,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            subscribe = get_object_or_404(Follow, user=user)
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = SignUpSerializer(data=request.data)
    email = request.data.get('email')
    if serializer.is_valid():
        user = get_object_or_404(User, email=email)
        if user:
            token = AccessToken.for_user(user)
            return Response(
                {'auth_token': f'{token}'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
